# 1. Brand Guidelines
brand_guidelines = {
    "product_name": "Cymbal Pod",
    "aesthetics": "Sleek, minimalist, futuristic with a touch of organic design. Think smooth curves, reflective surfaces, and integrated lighting. Inspired by nature and advanced technology.",
    "values": "Sustainability, personal freedom, urban efficiency, quiet innovation, community connection.",
    "mood_color_palette": "Calm and serene (blues, greens, silvers) with occasional vibrant accents (electric teal, soft gold). Overall feeling of tranquility and effortless movement. Think 'urban oasis' meets 'silent flight'.",
    "target_audience": "Urban professionals and creatives, 25-45 years old, who value efficiency, personal space, environmental consciousness, and cutting-edge design. They are early adopters of technology and seek seamless integration of their lifestyle with their commute."
}

# 2. Protagonist Description
protagonist_description = {
    "name": "Anya Sharma",
    "age": 32,
    "occupation": "Architect specializing in sustainable urban development",
    "appearance": "Medium height, athletic build, with sharp, intelligent eyes. She often wears practical yet stylish clothing in muted tones, reflecting her appreciation for functional design. Her hair is usually tied back in a neat bun, emphasizing her focused demeanor.",
    "personality": "Driven, innovative, thoughtful, and slightly introverted. Anya is passionate about creating better urban environments and finds solace and inspiration in her quiet commute. She is observant and appreciates the subtle beauty of the city.",
    "motivation": "To design and build cities that are harmonious with nature and efficient for their inhabitants. She seeks solutions that reduce urban sprawl and promote sustainable living. The Cymbal Pod is her tool for navigating the city without contributing to its noise or pollution."
}

# 3. Overall Narrative: (3-Scene Script)
narrative_script = [
    {
        "scene_number": 1,
        "title": "The Morning Commute: A Symphony of Silence",
        "description": "Anya wakes up in her minimalist, sun-drenched apartment overlooking a bustling cityscape. Instead of the usual rush, she calmly sips her tea. She then steps onto her Cymbal Pod, which silently glides out of her apartment building's integrated launchpad. The scene emphasizes the contrast between the chaotic city below and Anya's serene, effortless journey above the traffic. She passes by other commuters stuck in gridlock, a faint smile on her face as she enjoys the quiet hum of her pod and the panoramic views."
    },
    {
        "scene_number": 2,
        "title": "Urban Exploration: Connecting with the City",
        "description": "Anya uses her Cymbal Pod to navigate through various parts of the city, observing architectural details and green spaces. She effortlessly hovers over a pedestrian-only market, then descends gently into a rooftop garden she designed. The pod's quiet operation allows her to fully immerse herself in the urban environment, noticing details others miss. She interacts briefly with a community gardener, sharing a moment of connection before continuing her journey. The scene highlights the pod's versatility and its ability to foster a deeper connection with the urban landscape."
    },
    {
        "scene_number": 3,
        "title": "The Visionary's Return: A Sustainable Future",
        "description": "As dusk settles, Anya returns to her office, the city lights twinkling below. She parks her Cymbal Pod in a communal charging station, seamlessly integrating it into the building's infrastructure. She looks out at the city, a sense of accomplishment and hope in her eyes. The final shot shows Anya sketching new designs, with the Cymbal Pod visible in the background, symbolizing a future where urban transport is quiet, clean, and connected. A tagline appears on screen."
    }
]

# 4. Tagline
tagline = "Cymbal Pod: Glide Through Tomorrow. Today."

# Print all the generated content
print("--- Brand Guidelines ---")
print(f"Product Name: {brand_guidelines['product_name']}")
print(f"Aesthetics: {brand_guidelines['aesthetics']}")
print(f"Values: {brand_guidelines['values']}")
print(f"Mood/Color Palette: {brand_guidelines['mood_color_palette']}")
print(f"Target Audience: {brand_guidelines['target_audience']}")
print("\n--- Protagonist Description ---")
print(f"Name: {protagonist_description['name']}")
print(f"Age: {protagonist_description['age']}")
print(f"Occupation: {protagonist_description['occupation']}")
print(f"Appearance: {protagonist_description['appearance']}")
print(f"Personality: {protagonist_description['personality']}")
print(f"Motivation: {protagonist_description['motivation']}")
print("\n--- Overall Narrative (3-Scene Script) ---")
for scene in narrative_script:
    print(f"Scene {scene['scene_number']}: {scene['title']}")
    print(f"  Description: {scene['description']}")
print("\n--- Tagline ---")
print(tagline)
