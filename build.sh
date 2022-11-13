#/bin/sh

glslc shaders/shader.vert -o shaders/vert.spv

glslc shaders/shader.geom -o shaders/geom.spv

glslc shaders/shader.frag -o shaders/frag.spv

#python3 main.py

python3 main.py --width 1400 --height 1400 --layout mediumClassic.npy --agent UnpaintedAgent --heuristic unPaintedInconsistentHeuristic --function aStarSearch