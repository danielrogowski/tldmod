uniform sampler2D diffuse_texture;
varying vec4 outColor0;
varying vec3 outTexCoord;

void main ()
{
    vec2     uv = outTexCoord.xy;
    vec4 sample = texture2D(diffuse_texture, uv);
    float  bord = clamp((1.0-sample.r)*2.0,0.,1.);

    float bordColor = outTexCoord.z;
    gl_FragColor.a  = outColor0.a *(bord*(0.40+0.30*(1.0-sample.g)) + sample.a);


    float dist = texture2D( diffuse_texture, uv ).r;
    float isB = (1.0-sample.a) * (1.0-0.0);
    float width = fwidth(dist);
    gl_FragColor.rgb = outColor0.rgb * (1.0-isB) + vec3(bordColor,bordColor,bordColor)*(isB);
}
