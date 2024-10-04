#version 430

layout (location = 0) in vec4 in_position;
layout (location = 1) in vec4 in_velocity;  // New input for velocity

uniform mat4 projection;

out vec3 velocity;  // Pass velocity to the fragment shader

void main() {
    // Apply logarithm to the absolute value of the position components and restore sign
    vec3 logged_position = sign(in_position.xyz) * log(abs(in_position.xyz) + 1.0);  // Add 1.0 to avoid log(0)

    // Set the final position using the logarithmically transformed coordinates
    gl_Position = projection * vec4(logged_position, 1.0);

    // Pass velocity to fragment shader
    velocity = in_velocity.xyz;  // Pass only xyz part (velocity) to the fragment shader

    // Set the point size
    gl_PointSize = 1;
}
