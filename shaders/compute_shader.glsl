#version 430

layout (local_size_x = 512) in;

struct Particle {
    vec4 position;  // xyz = position, w = mass
    vec4 velocity;  // xyz = velocity
};

layout (std430, binding = 0) buffer PositionBuffer {
    vec4 positions[];
};

layout (std430, binding = 1) buffer VelocityBuffer {
    vec4 velocities[];
};

uniform float dt;
uniform int num_particles;
uniform float G;
float min_distance = 1;

void main() {
    uint i = gl_GlobalInvocationID.x;
    if (i >= num_particles) return;

    vec3 pos_i = positions[i].xyz;
    vec3 vel_i = velocities[i].xyz;
    vec3 force = vec3(0.0);

    for (uint j = 0; j < num_particles; j++) {
        if (i == j) continue;

        vec3 pos_j = positions[j].xyz;
        vec3 diff = pos_j - pos_i;
        float dist = length(diff);
        float dist2 = dot(diff, diff);
        float softening = min_distance * min_distance;
        float force_mag = (G * positions[j].w * 2.0) / (dist2 + softening);
        force += normalize(diff) * force_mag;
    }

    vec3 new_velocity = vel_i + force * dt;
    vec3 new_position = pos_i + new_velocity * dt;

    velocities[i].xyz = new_velocity;
    positions[i].xyz = new_position;
}