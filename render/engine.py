from config import *
from vlogging import logger, make_debug_messenger
from render import (
    InputBundle,
    create_graphics_pipeline,
    make_instance,
    choose_physical_device,
    create_logical_device,
    get_queues,
    create_swapchain,
    FramebufferInput,
    make_framebuffers,
    CommandbufferInputChunk,
    CommandPoolInputChunk,
    make_frame_command_buffers,
    make_command_pool,
    make_command_buffer,
    make_fence,
    make_semaphore,
)

import render.sync as sync
import vertex_object


class Engine:
    def __init__(self, width, height, window, scene):

        # glfw window parameters
        self.width = width
        self.height = height

        self.window = window

        self.scene = scene

        logger.print("Making a graphics engine")

        self.make_instance()
        self.make_device()
        self.make_pipeline()
        self.finalize_setup()
        self.make_assets()

    def make_instance(self):

        self.instance = make_instance("GridWorld")

        if logger.debug_mode:
            self.debugMessenger = make_debug_messenger(self.instance)

        c_style_surface = ffi.new("VkSurfaceKHR*")
        if (
            glfw.create_window_surface(
                instance=self.instance,
                window=self.window,
                allocator=None,
                surface=c_style_surface,
            )
            != VK_SUCCESS
        ):
            logger.print("Failed to abstract glfw's surface for vulkan")
        else:
            logger.print("Successfully abstracted glfw's surface for vulkan")
        self.surface = c_style_surface[0]

    def make_device(self):

        self.physicalDevice = choose_physical_device(self.instance)
        self.device = create_logical_device(
            physicalDevice=self.physicalDevice,
            instance=self.instance,
            surface=self.surface,
        )
        queues = get_queues(
            physicalDevice=self.physicalDevice,
            logicalDevice=self.device,
            instance=self.instance,
            surface=self.surface,
        )
        self.graphicsQueue = queues[0]
        self.presentQueue = queues[1]

        self.make_swapchain()

        self.frameNumber = 0

    def make_swapchain(self):
        """
        Makes the engine's swapchain, note that this will make images
        and image views, it won't make frames ready for rendering.
        """

        bundle = create_swapchain(
            self.instance,
            self.device,
            self.physicalDevice,
            self.surface,
            self.width,
            self.height,
        )

        self.swapchain = bundle.swapchain
        self.swapchainFrames = bundle.frames
        self.swapchainFormat = bundle.format
        self.swapchainExtent = bundle.extent
        self.maxFramesInFlight = len(self.swapchainFrames)

    def recreate_swapchain(self, resize=False):
        """
        Destroy the current swapchain, then rebuild a new one
        """
        if resize:
            self.width, self.height = glfw.get_window_size(self.window)
        else:
            self.width = 0
            self.height = 0
            while self.width == 0 or self.height == 0:
                self.width, self.height = glfw.get_window_size(self.window)
                glfw.wait_events()

        vkDeviceWaitIdle(self.device)
        self.cleanup_swapchain()

        self.make_swapchain()
        self.make_framebuffers()
        self.make_command_buffers()
        self.make_frame_sync_objects()

    def make_pipeline(self):

        inputBundle = InputBundle(
            device=self.device,
            scene=self.scene,
            swapchainImageFormat=self.swapchainFormat,
            swapchainExtent=self.swapchainExtent,
            vertexFilepath="shaders/vert.spv",
            geometryFilepath="shaders/geom.spv",
            fragmentFilepath="shaders/frag.spv",
        )

        outputBundle = create_graphics_pipeline(inputBundle)

        self.pipelineLayout = outputBundle.pipelineLayout
        self.renderpass = outputBundle.renderPass
        self.pipeline = outputBundle.pipeline

    def make_framebuffers(self):
        """
        Makes a framebuffer for each frame on the swapchain.
        """

        framebufferInput = FramebufferInput()
        framebufferInput.device = self.device
        framebufferInput.renderpass = self.renderpass
        framebufferInput.swapchainExtent = self.swapchainExtent
        make_framebuffers(framebufferInput, self.swapchainFrames)

    def make_command_buffers(self):
        """
        Make a command buffer for each frame on the swapchain.
        """

        commandbufferInput = CommandbufferInputChunk()
        commandbufferInput.device = self.device
        commandbufferInput.commandPool = self.commandPool
        commandbufferInput.frames = self.swapchainFrames
        make_frame_command_buffers(commandbufferInput)

    def make_frame_sync_objects(self):
        """
        Make the semaphores and fences needed to render each frame.
        """

        for frame in self.swapchainFrames:
            frame.inFlight = sync.make_fence(self.device)
            frame.imageAvailable = sync.make_semaphore(self.device)
            frame.renderFinished = sync.make_semaphore(self.device)

    def finalize_setup(self):

        self.make_framebuffers()

        commandPoolInput = CommandPoolInputChunk()
        commandPoolInput.device = self.device
        commandPoolInput.physicalDevice = self.physicalDevice
        commandPoolInput.surface = self.surface
        commandPoolInput.instance = self.instance
        self.commandPool = make_command_pool(commandPoolInput)

        commandbufferInput = CommandbufferInputChunk()
        commandbufferInput.device = self.device
        commandbufferInput.commandPool = self.commandPool
        commandbufferInput.frames = self.swapchainFrames
        self.mainCommandbuffer = make_command_buffer(commandbufferInput)
        make_frame_command_buffers(commandbufferInput)

        self.make_frame_sync_objects()

    def make_assets(self):

        self.meshes = vertex_object.VertexObject()

        self.meshes.consume(SCENE, self.scene.vertices, self.scene.vertex_size)

        self.meshes.consume(AGENTS, self.scene.agents_vertex, self.scene.vertex_size)


        finalization_chunk = vertex_object.VertexBufferFinalizationStruct()
        finalization_chunk.command_buffer = self.mainCommandbuffer
        finalization_chunk.logical_device = self.device
        finalization_chunk.physical_device = self.physicalDevice
        finalization_chunk.queue = self.graphicsQueue

        self.meshes.finalize(finalization_chunk)
        self.scene.vertices = self.meshes.recover_view(SCENE, self.scene.vertex_size)
        self.scene.agents_vertex = self.meshes.recover_view(
            AGENTS, self.scene.vertex_size
        )

    def prepare_scene(self, commandBuffer):

        vkCmdBindVertexBuffers(
            commandBuffer=commandBuffer,
            firstBinding=0,
            bindingCount=1,
            pBuffers=(self.meshes.vertex_buffer.buffer,),
            pOffsets=(0,),
        )

    def record_draw_commands(self, commandBuffer, imageIndex):

        beginInfo = VkCommandBufferBeginInfo()

        try:
            vkBeginCommandBuffer(commandBuffer, beginInfo)
        except:
            logger.print("Failed to begin recording command buffer")

        renderpassInfo = VkRenderPassBeginInfo(
            renderPass=self.renderpass,
            framebuffer=self.swapchainFrames[imageIndex].framebuffer,
            renderArea=[[0, 0], self.swapchainExtent],
        )

        clearColor1 = VkClearValue(color=[[0.1, 0.1, 0.1, 1.0]])

        depthStencil = VkClearDepthStencilValue(depth=1.0, stencil=0)
        clearColor2 = VkClearValue(depthStencil=depthStencil)

        arr = ffi.new("VkClearValue[2]", [clearColor1, clearColor2])
        renderpassInfo.clearValueCount = 2
        renderpassInfo.pClearValues = arr  # ffi.addressof(clearColor1)

        vkCmdBeginRenderPass(commandBuffer, renderpassInfo, VK_SUBPASS_CONTENTS_INLINE)

        viewport = VkViewport(
            x=0,
            y=0,
            width=self.swapchainExtent.width,
            height=self.swapchainExtent.height,
            minDepth=0.0,
            maxDepth=1.0,
        )

        # transformation from image to framebuffer: cutout
        scissor = VkRect2D(offset=[0, 0], extent=self.swapchainExtent)

        vkCmdSetViewport(commandBuffer, 0, 1, (viewport,))
        vkCmdSetScissor(commandBuffer, 0, 1, (scissor,))

        vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, self.pipeline)

        self.prepare_scene(commandBuffer)
        vertexCount = self.meshes.sizes[SCENE]
        # for position in scene.triangle_positions:
        model_transform = np.array(self.scene.push_constant, dtype=np.float32)
        # model_transform = pyrr.matrix44.create_from_translation(vec = scene.color, dtype = np.float32)
        objData = ffi.cast("float *", ffi.from_buffer(model_transform))
        vkCmdPushConstants(
            commandBuffer=commandBuffer,
            layout=self.pipelineLayout,
            stageFlags=VK_SHADER_STAGE_VERTEX_BIT
            | VK_SHADER_STAGE_GEOMETRY_BIT
            | VK_SHADER_STAGE_FRAGMENT_BIT,
            offset=0,
            size=4 * self.scene.push_constant_size,
            pValues=objData,
        )
        vkCmdDraw(
            commandBuffer=commandBuffer,
            vertexCount=vertexCount,
            instanceCount=1,
            firstVertex=0,
            firstInstance=0,
        )

        firstVertex = self.meshes.offsets[AGENTS]
        vertexCount = self.meshes.sizes[AGENTS]
        for i, position in enumerate(self.scene.agents_positions):
            firstVertex += i
            x, y = self.scene.position((position[1], position[0]))
            model_transform = np.array(
                self.scene.get_push_constant([x, y]), dtype=np.float32
            )

            objData = ffi.cast("float *", ffi.from_buffer(model_transform))
            vkCmdPushConstants(
                commandBuffer=commandBuffer,
                layout=self.pipelineLayout,
                stageFlags=VK_SHADER_STAGE_VERTEX_BIT
                | VK_SHADER_STAGE_GEOMETRY_BIT
                | VK_SHADER_STAGE_FRAGMENT_BIT,
                offset=0,
                size=4 * self.scene.push_constant_size,
                pValues=objData,
            )
            vkCmdDraw(
                commandBuffer=commandBuffer,
                vertexCount=1,
                instanceCount=1,
                firstVertex=firstVertex,
                firstInstance=0,
            )

        vkCmdEndRenderPass(commandBuffer)

        try:
            vkEndCommandBuffer(commandBuffer)
        except:
            logger.print("Failed to end recording command buffer")

    def render(self):

        # grab instance procedures
        vkAcquireNextImageKHR = vkGetDeviceProcAddr(
            self.device, "vkAcquireNextImageKHR"
        )
        vkQueuePresentKHR = vkGetDeviceProcAddr(self.device, "vkQueuePresentKHR")

        vkWaitForFences(
            device=self.device,
            fenceCount=1,
            pFences=[
                self.swapchainFrames[self.frameNumber].inFlight,
            ],
            waitAll=VK_TRUE,
            timeout=1000000000,
        )
        vkResetFences(
            device=self.device,
            fenceCount=1,
            pFences=[
                self.swapchainFrames[self.frameNumber].inFlight,
            ],
        )
        if self.scene.dirty:
            finalization_chunk = vertex_object.VertexBufferFinalizationStruct()
            finalization_chunk.command_buffer = self.mainCommandbuffer
            finalization_chunk.logical_device = self.device
            finalization_chunk.physical_device = self.physicalDevice
            finalization_chunk.queue = self.graphicsQueue
            self.meshes.update(finalization_chunk)

        try:
            imageIndex = vkAcquireNextImageKHR(
                device=self.device,
                swapchain=self.swapchain,
                timeout=1000000000,
                semaphore=self.swapchainFrames[self.frameNumber].imageAvailable,
                fence=VK_NULL_HANDLE,
            )
        except:
            logger.print("recreate swapchain")
            self.recreate_swapchain()
            return

        commandBuffer = self.swapchainFrames[self.frameNumber].commandbuffer
        vkResetCommandBuffer(commandBuffer=commandBuffer, flags=0)
        self.record_draw_commands(commandBuffer, imageIndex)

        submitInfo = VkSubmitInfo(
            waitSemaphoreCount=1,
            pWaitSemaphores=[
                self.swapchainFrames[self.frameNumber].imageAvailable,
            ],
            pWaitDstStageMask=[
                VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
            ],
            commandBufferCount=1,
            pCommandBuffers=[
                commandBuffer,
            ],
            signalSemaphoreCount=1,
            pSignalSemaphores=[
                self.swapchainFrames[self.frameNumber].renderFinished,
            ],
        )

        try:
            vkQueueSubmit(
                queue=self.graphicsQueue,
                submitCount=1,
                pSubmits=submitInfo,
                fence=self.swapchainFrames[self.frameNumber].inFlight,
            )
        except:
            logger.print("Failed to submit draw commands")

        presentInfo = VkPresentInfoKHR(
            waitSemaphoreCount=1,
            pWaitSemaphores=[
                self.swapchainFrames[self.frameNumber].renderFinished,
            ],
            swapchainCount=1,
            pSwapchains=[
                self.swapchain,
            ],
            pImageIndices=[
                imageIndex,
            ],
        )

        try:
            vkQueuePresentKHR(self.presentQueue, presentInfo)
        except:
            logger.print("recreate swapchain")
            self.recreate_swapchain()
            return

        self.frameNumber = (self.frameNumber + 1) % self.maxFramesInFlight

    def cleanup_swapchain(self):
        """
        Free the memory allocated for each frame, and destroy the swapchain.
        """

        for frame in self.swapchainFrames:
            vkDestroyImageView(
                device=self.device, imageView=frame.image_view, pAllocator=None
            )
            vkDestroyFramebuffer(
                device=self.device, framebuffer=frame.framebuffer, pAllocator=None
            )
            vkDestroyFence(self.device, frame.inFlight, None)
            vkDestroySemaphore(self.device, frame.imageAvailable, None)
            vkDestroySemaphore(self.device, frame.renderFinished, None)

        destructionFunction = vkGetDeviceProcAddr(self.device, "vkDestroySwapchainKHR")
        destructionFunction(self.device, self.swapchain, None)

    def close(self):

        vkDeviceWaitIdle(self.device)

        logger.print("Goodbye see you!\n")

        vkDestroyCommandPool(self.device, self.commandPool, None)

        vkDestroyPipeline(self.device, self.pipeline, None)
        vkDestroyPipelineLayout(self.device, self.pipelineLayout, None)
        vkDestroyRenderPass(self.device, self.renderpass, None)

        self.cleanup_swapchain()

        self.meshes.destroy()

        vkDestroyDevice(device=self.device, pAllocator=None)

        destructionFunction = vkGetInstanceProcAddr(
            self.instance, "vkDestroySurfaceKHR"
        )
        destructionFunction(self.instance, self.surface, None)
        if logger.debug_mode:
            # fetch destruction function
            destructionFunction = vkGetInstanceProcAddr(
                self.instance, "vkDestroyDebugReportCallbackEXT"
            )

            """
                def vkDestroyDebugReportCallbackEXT(
                    instance
                    ,callback
                    ,pAllocator
                ,):
            """
            destructionFunction(self.instance, self.debugMessenger, None)
        """
            from _vulkan.py:

            def vkDestroyInstance(
                instance,
                pAllocator,
            )
        """
        vkDestroyInstance(self.instance, None)

        # terminate glfw
        glfw.terminate()
