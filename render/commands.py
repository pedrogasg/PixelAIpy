from config import *
from render import find_queue_families
from vlogging import logger

class CommandPoolInputChunk:


    def __init__(self):

        self.device = None
        self.physicalDevice = None
        self.surface = None
        self.instance = None

class CommandbufferInputChunk:


    def __init__(self):

        self.device = None
        self.commandPool = None
        self.frames = None

def make_command_pool(inputChunk):

    queueFamilyIndices = find_queue_families(
        device = inputChunk.physicalDevice,
        instance = inputChunk.instance,
        surface = inputChunk.surface,
    )

    poolInfo = VkCommandPoolCreateInfo(
        queueFamilyIndex=queueFamilyIndices.graphicsFamily,
        flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT
    )

    try:
        commandPool = vkCreateCommandPool(
            inputChunk.device, poolInfo, None
        )
        logger.print("Created command pool")
        return commandPool
    except:

        logger.print("Failed to create command pool")
        return None

def make_frame_command_buffers(inputChunk: CommandbufferInputChunk) -> None:
    """
        Make command buffers for each frame.

        Parameters:
            inputChunk (commandBufferInputChunk): holds the various objects
                                                    needed.
    """

    allocInfo = VkCommandBufferAllocateInfo(
        commandPool = inputChunk.commandPool,
        level = VK_COMMAND_BUFFER_LEVEL_PRIMARY,
        commandBufferCount = 1
    )

    #Make a command buffer for each frame
    for i,frame in enumerate(inputChunk.frames):

        try:
            frame.commandbuffer = vkAllocateCommandBuffers(inputChunk.device, allocInfo)[0]

            logger.print(f"Allocated command buffer for frame {i}")
        except:
            logger.print(f"Failed to allocate command buffer for frame {i}")

def make_command_buffer(inputChunk):

    """
        Make a single command buffer for each frame.

        Parameters:
            inputChunk (commandBufferInputChunk): holds the various objects
                                                    needed.
    """

    allocInfo = VkCommandBufferAllocateInfo(
        commandPool = inputChunk.commandPool,
        level = VK_COMMAND_BUFFER_LEVEL_PRIMARY,
        commandBufferCount = 1
    )
    
    try:
        commandbuffer = vkAllocateCommandBuffers(inputChunk.device, allocInfo)[0]

        logger.print("Allocated main command buffer")
        
        return commandbuffer
    except:
        logger.print("Failed to allocate main command buffer")
        
        return None