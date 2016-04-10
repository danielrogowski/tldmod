/* tld glsl shader -- vs_font_mtarini -- by swyter */

uniform vec4 vMaterialColor;
uniform float fFogDensity;
uniform mat4 matWorldViewProj;
uniform mat4 matWorldView;
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
varying vec4 outColor0;
varying vec3 outTexCoord;
varying float outFog;
void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = inPosition;
  gl_Position = (matWorldViewProj * tmpvar_1);
  vec4 tmpvar_2;
  tmpvar_2.w = 1.0;
  tmpvar_2.xyz = inPosition;
  vec3 tmpvar_3;
  tmpvar_3 = (matWorldView * tmpvar_2).xyz;
  outColor0 = inColor0.bgra * vMaterialColor;

  // compute border color
  outTexCoord.xy = inTexCoord;
  outTexCoord.z = float( (max(outColor0.r, max( outColor0.g, outColor0.b ) ) >0.5)?0:1 );

  outFog = (1.0/(exp2((
    sqrt(dot (tmpvar_3, tmpvar_3))
   * fFogDensity))));
}

