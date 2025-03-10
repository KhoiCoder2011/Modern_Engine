#version 330 core

out vec4 fragColor;       // Output color

in vec2 uv_0;
in vec3 v_normal;
in vec3 v_fragPos;
in vec3 frag_color;       // Material color (diffuse)

uniform sampler2D tex_0;

void main() {
    vec4 tex_color = texture(tex_0, uv_0); // Get texture color
    fragColor = tex_color * vec4(frag_color, 1.0); // Multiply texture and fragment colors
}
