from config import *
import memory

class VertexBufferFinalizationStruct:

    
    def __init__(self):

        self.logical_device = None
        self.physical_device = None
        self.command_buffer = None
        self.queue = None

class VertexObject:

    
    def __init__(self):

        self.offset = 0
        self.offsets = {}
        self.sizes = {}
        self.data_sizes = {}
        self.lump = np.array([],dtype=np.float32)
    
    def consume(self, meshType, vertexData, vertex_size):

        self.lump = np.append(self.lump, vertexData)
        data_size = vertexData.size
        vertexCount = int(data_size // vertex_size)
        
        self.data_sizes[meshType] = data_size
        self.offsets[meshType] = self.offset
        self.sizes[meshType] = vertexCount
        self.offset += vertexCount

    def recover_view(self, meshType, vertex_size):
        initial_offset = self.offsets[meshType] * vertex_size
        data_size = self.data_sizes[meshType]
        return self.lump[initial_offset:data_size]

    @classmethod
    def _input_for_staging(cls, lump, finalization_chunk):
        input_chunk = memory.BufferInput()
        input_chunk.logical_device = finalization_chunk.logical_device
        input_chunk.physical_device = finalization_chunk.physical_device
        input_chunk.size = lump.nbytes
        input_chunk.usage = VK_BUFFER_USAGE_TRANSFER_SRC_BIT
        input_chunk.memory_properties = \
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        return input_chunk

    @classmethod    
    def _create_staging_buffer(cls, lump, input_chunk, finalization_chunk):

        staging_buffer = memory.create_buffer(input_chunk)
        memory_location = vkMapMemory(
            device = finalization_chunk.logical_device, memory = staging_buffer.buffer_memory, 
            offset = 0, size = input_chunk.size, flags = 0
        )
        # (location to move to, data to move, size in bytes)
        ffi.memmove(memory_location, lump, input_chunk.size)
        vkUnmapMemory(device = finalization_chunk.logical_device, memory = staging_buffer.buffer_memory)

        return staging_buffer

    def update(self, finalization_chunk):
        input_chunk = VertexObject._input_for_staging(self.lump, finalization_chunk)

        staging_buffer = VertexObject._create_staging_buffer(self.lump, input_chunk, finalization_chunk)

        memory.copy_buffer(
            src_buffer = staging_buffer, dst_buffer = self.vertex_buffer,
            size = input_chunk.size, queue = finalization_chunk.queue,
            command_buffer = finalization_chunk.command_buffer
        )

        VertexObject._destroy_buffer(self.logical_device, staging_buffer)
    
    def finalize(self, finalization_chunk):

        self.logical_device = finalization_chunk.logical_device

        input_chunk = VertexObject._input_for_staging(self.lump, finalization_chunk)

        staging_buffer = VertexObject._create_staging_buffer(self.lump, input_chunk, finalization_chunk)

        input_chunk.usage = \
            VK_BUFFER_USAGE_TRANSFER_DST_BIT | VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
        input_chunk.memory_properties = VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
        self.vertex_buffer = memory.create_buffer(input_chunk)

        memory.copy_buffer(
            src_buffer = staging_buffer, dst_buffer = self.vertex_buffer,
            size = input_chunk.size, queue = finalization_chunk.queue,
            command_buffer = finalization_chunk.command_buffer
        )

        VertexObject._destroy_buffer(self.logical_device, staging_buffer)

    @classmethod
    def _destroy_buffer(cls, logical_device, buffer):
        vkDestroyBuffer(
            device = logical_device, buffer = buffer.buffer, 
            pAllocator = None
        )
        vkFreeMemory(
            device = logical_device, 
            memory = buffer.buffer_memory, pAllocator = None
        )
    
    def destroy(self):
        VertexObject._destroy_buffer(self.logical_device, self.vertex_buffer)
