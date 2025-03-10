#version 330 core

layout(location = 0) in vec3 in_vert;
layout(location = 1) in vec3 in_color;
layout(location = 2) in vec2 in_uv;
layout(location = 3) in vec3 in_normal;

out vec3 frag_color;
out vec3 v_normal;
out vec3 v_fragPos;

out vec2 uv_0;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;

void main() {
    frag_color = in_color;
    uv_0 = in_uv;
    gl_Position = m_proj * m_view * m_model * vec4(in_vert, 1.0);
    v_fragPos = vec3(m_model * vec4(in_vert, 1.0));
    v_normal = mat3(transpose(inverse(m_model))) * in_normal;
}