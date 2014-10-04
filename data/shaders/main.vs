#version 330

layout(location = 0) in vec2 position;
//layout(location=1) in vec4 vertColor

uniform mat4 ortho;
uniform mat4 model;

mat4 mvp;

void main()
{	
	mvp = ortho * model;
	gl_Position = mvp * vec4( position, 1.0, 1.0 );

}