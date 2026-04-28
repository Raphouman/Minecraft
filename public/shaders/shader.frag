#version 330 core

uniform sampler2D tex;
in vec3 c;
in vec2 vtex;

// in vec3 color; // Couleur interpolée de l'input
out vec4 color; // Couleur de sortie
void main()
{
    vec4 color_texture = texture(tex, vtex);
    vec4 color_final = vec4(c, 0.0)*color_texture;

    color = color_final;
}