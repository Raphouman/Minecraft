#version 330 core

out vec4 color;

in vec3 coordonnee_3d;
in vec3 p;
in vec3 normal_out;
in vec3 c;
in vec2 vtex;

uniform mat4 view;
uniform sampler2D tex;

void main (void)
{
    vec3 light = vec3(0.5, 50, 5.0);

    vec3 n = normalize(normal_out);
    vec3 d = normalize(light - p);
    vec3 r = reflect(-d, n);
    vec3 o = normalize(-p);

    float diffuse  = 0.6 * clamp(dot(n, d), 0.0, 1.0);
    float specular = 0.15 * pow(clamp(dot(r, o), 0.0, 1.0), 128.0);
    float ambiant  = 0.2;

    vec4 white = vec4(1.0, 1.0, 1.0, 1.0);
    vec4 color_texture = texture(tex, vtex);
    vec4 color_final = vec4(c, 1.0) * color_texture;

    color = (ambiant + diffuse) * color_final + specular * white;
    // color = vec4(1.0, 0.0, 0.0, 1.0); 
}
