<!-- Intro -->
# **CLANK_ASSISTANT**
> **Lucas Arroyo Blanco**  
> 
> _PatoOsoPatoso_  

&nbsp;

<!-- Index -->
# Table of contents
## &nbsp;&nbsp;&nbsp;&nbsp;1&nbsp;)&nbsp;&nbsp;[Description](#description)
## &nbsp;&nbsp;&nbsp;&nbsp;2&nbsp;)&nbsp;&nbsp;[Requirements](#requirements) 
## &nbsp;&nbsp;&nbsp;&nbsp;3&nbsp;)&nbsp;&nbsp;[Modifications to be used](#modifications-to-be-used)  

&nbsp;  
&nbsp; 

<!-- Description -->
## **Description**

Clank is designed to be like a voice assistant that has predefined commands for you to ask him to execute, like open files for example (currently the only actual functionality)

The model is currently in spanish but that can be changed by downloading an other [vosk model](https://alphacephei.com/vosk/models).  
I used [this](https://alphacephei.com/vosk/models/vosk-model-small-es-0.3.zip) one.  

[ IMPORTANT ]  
The linux implementation is still in progress because I use the voices that come installed when you choose a language on Windows.

I am ver aware of the lack of features that this "voice assistant" has, the only excuse that I can give is that I am not able to find more tasks for this.

&nbsp;  

<!-- Requirements -->
## **Requirements**
Like I said previously you need a vosk model like the one I have in [audio](audio/).  

An other requirement is having an IBM speech recognition authentication and service url. You can create an account for IBM Watson [here](https://cloud.ibm.com/catalog/services/text-to-speech).

&nbsp;

<!-- Modifications -->
## **Modifications to be used**
To use the code as it is right now first you are going to need to create a **.env** file.  
The file should look like this:  
&nbsp;
```
IBM_AUTH=
SERVICE_URL=
```  
Fill `IBM_AUTH` with the authenticator of your account and `SERVICE_URL` with the service_url you are given. 
&nbsp;  
&nbsp;

<!-- Bye bye -->
<img src="https://static.wikia.nocookie.net/horadeaventura/images/c/c2/CaracolRJS.png/revision/latest?cb=20140518032802&path-prefix=es" alt="drawing" style="width:100px;"/>**_bye bye_**