#version 430

layout (local_size_x = 512) in;

struct Particle {
    vec4 position;  // xyz = position, w = mass
    vec4 velocity;  // xyz = velocity, w is unused
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
uniform float min_distance;

void main() {
    uint i = gl_GlobalInvocationID.x;
    if (i >= num_particles) return;

    vec3 pos_i = positions[i].xyz;
    vec3 vel_i = velocities[i].xyz;
    float mass_i = positions[i].w;
    vec3 force = vec3(0.0);

    for (uint j = 0; j < num_particles; j++) {
        if (i == j) continue;

        vec3 pos_j = positions[j].xyz;
        float mass_j = positions[j].w;

        // Calculate distance between particles i and j
        vec3 diff = pos_j - pos_i;
        float dist = length(diff);
        float dist2 = dot(diff, diff);  // This is dist^2

        // Softening factor to avoid singularity
        float softening = min_distance * min_distance;

        // Calculate the force magnitude (similar to C++ version)
        float force_mag = (G * mass_i * mass_j) / (dist2 + softening);

        // Calculate the directional force vector (normalize distance and scale by force)
        vec3 force_direction = normalize(diff);
        force += force_direction * force_mag * 0.99;
    }

    // Update velocity and position based on the calculated force
    vec3 new_velocity = vel_i + force * dt;
    vec3 new_position = pos_i + vel_i * dt + 0.5 * force * dt * dt;

    velocities[i].xyz = new_velocity;
    positions[i].xyz = new_position;
}
