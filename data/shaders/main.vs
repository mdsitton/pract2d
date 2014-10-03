#version 330

layout(location=0) in vec3 vertPosition;
//layout(location=1) in vec4 vertColor

uniform mat3 ortho;
uniform mat4 model;

void main()
{	
	vec3 mvp = ortho * model;
	gl_position = ortho * vec4( model * vertPosition, 1.0 );

}