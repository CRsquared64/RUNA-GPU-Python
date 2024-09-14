#version 430

#define EPSILON 1
layout (local_size_x = 512) in;

struct Particle {
    vec4 position;
    vec4 velocity;
};

layout (std430, binding = 0) buffer Particles {
    Particle particles[];
};

uniform float dt;
uniform int num_particles;
uniform float G;

void main() {
    uint i = gl_GlobalInvocationID.x;
    if (i >= num_particles) return;

    vec3 pos_i = particles[i].position.xyz;
    vec3 vel_i = particles[i].velocity.xyz;
    vec3 force = vec3(0.0);

    for (uint j = 0; j < num_particles; j++) {
        if (i == j) continue;

        vec3 pos_j = particles[j].position.xyz;
        vec3 diff = pos_j - pos_i;
        float dist = length(diff) + EPSILON;
        float force_mag = (G / (dist * dist)) * particles[j].position.w; // Mass in .w
        force += normalize(diff) * force_mag;
    }

    vel_i += force * dt;
    pos_i += vel_i * dt;

    particles[i].position.xyz = pos_i;
    particles[i].velocity.xyz = vel_i;
}
