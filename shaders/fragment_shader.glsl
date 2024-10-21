#version 430

in vec3 velocity;  // Velocity passed from vertex shader

out vec4 fragColor;

void main() {
    // Calculate the velocity magnitude (speed)
    float speed = length(velocity) * 0.0005;

    // Define base colors: blue for slow, white for medium, red for fast
    vec4 blue = vec4(0.8, 0.8, 1,0.1);  // Slow (blue)
    vec4 white = vec4(1.0, 1.0, 1.0,1.0);  // Medium speed (white)
    vec4 red = vec4(1.0, 0.8, 0.8,1.0);  // Fast (red)

    // Map speed to a range between 0 and 1
    float normalizedSpeed = clamp(speed * 10.0, 0.0, 1.0);

    // Blend between blue and white for slower speeds
    vec4 color = mix(blue, white, normalizedSpeed);

    // For faster speeds, blend between white and red
    if (normalizedSpeed > 0.5) {
        color = mix(white, red, (normalizedSpeed - 0.5) * 2.0);  // Blend between white and red for high speeds
    }

    // Set the final color
    fragColor = vec4(color);  // Alpha is 1.0 for fully opaque
}
