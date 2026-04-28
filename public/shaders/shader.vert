#version 330 core

uniform mat4 modelMatrix;
uniform mat4 projection;
uniform mat4 view;
//uniform mat4 camera_matrix;   
// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 color;
layout (location = 3) in vec2 texture;

out vec3 p;
out vec3 c;
out vec3 normal_out;
out vec2 vtex;

// Un Vertex Shader minimaliste
void main (void)
{
  // le passage du monde normalisé au monde gl_position
  // Coordonnees du sommet
  p = position;
  gl_Position = projection * view * modelMatrix * vec4(position,1.0);

  c = color;
  normal_out = normal;
  vtex = texture;
}
