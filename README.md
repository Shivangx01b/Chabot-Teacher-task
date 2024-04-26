# Chabot-Teacher-task
Chabot-Teacher-task


## How to run

- Step 1

```
docker build -t chatbot-teacher .
```

- Step 2

```
docker run -it -e OpenAI_Key="< add you gpt4 keys here" -p 8000:8000 chatbot-teacher
```

- Step 3 to call the text api
  
  - Request
      ```
      curl --location 'http://localhost:8000/chat/text' \
      --form 'user_input="What is area of a circle ?"'
      ```
  - Response
      ```
      {
    "response": " Sure, I'd be happy to help with that! The area of a circle is the measure of the surface enclosed by the circle. It is calculated by multiplying the square of the radius of the circle by pi (π), which is approximately 3.14. So, the formula for finding the area of a circle is A = πr^2, where A is the area and r is the radius. To find the area, simply square the radius and then multiply it by pi. For example, if the radius of a circle is 5 units, the area would be 25π square units. I hope that helps! Is there anything else I can assist you with?\n\nHere are some relevant YouTube videos for further reference:\n\n['https://www.youtube.com/watch?v=YokKp3pwVFc&pp=ygVAU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBXaGF0IGlzIGFyZWEgb2YgYSBjaXJjbGUgPw%3D%3D', 'https://www.youtube.com/watch?v=JC2kRM3jTOo&pp=ygVAU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBXaGF0IGlzIGFyZWEgb2YgYSBjaXJjbGUgPw%3D%3D']\n\nHere are some relevant YouTube videos for further reference:\n\n['https://www.youtube.com/watch?v=YokKp3pwVFc&pp=ygVAU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBXaGF0IGlzIGFyZWEgb2YgYSBjaXJjbGUgPw%3D%3D', 'https://www.youtube.com/watch?v=JC2kRM3jTOo&pp=ygVAU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBXaGF0IGlzIGFyZWEgb2YgYSBjaXJjbGUgPw%3D%3D']"
	}
     ```

- Step 4 to call image api

   - Request
     ```
     curl --location 'http://localhost:8000/chat/image' \
	--form 'image=@"/C:/Users/shivang/Desktop/image.PNG"'
     ```

   - Response
     ```
	     {
	    "response": " Sure, I'd be happy to help with that! First, let's break down the given equation: 16 + 4x = 10 + 14. We can simplify this to 4x = 24. Now, we can divide both sides by 4 to isolate x, giving us x = 6. So, the value of 8x would be 8 times 6, which is 48. Therefore, the correct answer is B) 6. Does that make sense?\n\nHere are some relevant YouTube videos for further reference:\n\n['https://www.youtube.com/watch?v=6OCkx2PIGjk&pp=ygUvU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBpbWFnZS5QTkc%3D', 'https://www.youtube.com/watch?v=s9pc1-qk-bE&pp=ygUvU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBpbWFnZS5QTkc%3D']\n\nHere are some relevant YouTube videos for further reference:\n\n['https://www.youtube.com/watch?v=6OCkx2PIGjk&pp=ygUvU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBpbWFnZS5QTkc%3D', 'https://www.youtube.com/watch?v=s9pc1-qk-bE&pp=ygUvU2VhcmNoIGZvciBZb3VUdWJlIHZpZGVvcyByZWxhdGVkIHRvOiBpbWFnZS5QTkc%3D']"
	}
     ```
      




## What we have
	
	- Abel to answer you qeustion 
		- Can take text
		- Can take images
		- Give text answers with reference youtube videos using live apis calls

	- Able to cache the old answers
		- Cache text
		- Cache video links
		- Cache image used

  - Comments added for each step.


## Improvements

	- Make code more modular (Using classes)
	- Feedback loop to improve prompt (more agents)
  - Make it async using redis and celery to handel scale
  - Keep track of history to retain old convertations and improve the context if need
