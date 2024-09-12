#version 430

out vec4 fragColour;

uniform vec2 res;
uniform float time;
uniform float k;
void main(){
    vec2 uv = (gl_FragCoord.xy - 0.5 * res.xy) / res.y;
    vec3 col = vec3(0.0);

    col += k / length(uv - 0.05);
    fragColour = vec4(col,1.0);
   }
