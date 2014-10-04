#version 330

layout(location = 0) in vec3 position;
//layout(location=1) in vec4 vertColor

uniform mat4 ortho;
uniform mat3 model;

mat3 mvp;

void main()
{	
	mvp = ortho * model;
	gl_Position = mvp * vec4( position, 1.0, 1.0 );

}