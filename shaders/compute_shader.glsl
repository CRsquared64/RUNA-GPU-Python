#version 430

layout (local_size_x = 512) in;

struct Particle {
    vec4 position;  // xyz = position, w = mass
    vec4 velocity;  // xyz = velocity
};

layout (std430, binding = 0) buffer Particles {
    Particle particles[];
};

uniform float dt;
uniform int num_particles;
uniform float G;
float min_distance = 1;

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
        float dist = length(diff);
        float dist2 = dot(diff, diff);
        float softening = min_distance * min_distance;
        float force_mag = (G * particles[j].position.w * 2) / (dist2 + softening);
        force += normalize(diff) * force_mag;
    }

    vel_i += force * dt;
    pos_i += vel_i * dt;

    particles[i].position.xyz = pos_i;
    particles[i].velocity.xyz = vel_i;
}
