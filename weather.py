from aima.logic import *
from aima.utils import *
import tkinter as tk
from PIL import Image, ImageTk


# Create an empty knowledge base
kb = FolKB()

# Add first-order logic clauses (rules and facts)

# Sky Condition Rules
kb.tell(expr("(SkyClear(x) & Sky(x)) ==> Weather(x, Sunny)"))
kb.tell(expr("(FewClouds(x) & Sky(x)) ==> Weather(x, PartlyCloudy)"))
kb.tell(expr("(Overcast(x) & Sky(x)) ==> Weather(x, Cloudy)"))

# Wind Rules
kb.tell(expr("(CalmWind(x) & Wind(x)) ==> Weather(x, Stable)"))
kb.tell(expr("(GentleBreeze(x) & Wind(x)) ==> Weather(x, Fair)"))
kb.tell(expr("(StrongWind(x) & Wind(x)) ==> Weather(x, Stormy)"))

# Temperature Rules
kb.tell(expr("(CoolTemp(x) & Temperature(x)) ==> Weather(x, Mild)"))
kb.tell(expr("(WarmTemp(x) & Temperature(x)) ==> Weather(x, Pleasant)"))
kb.tell(expr("(HotTemp(x) & Temperature(x)) ==> Weather(x, Heatwave)"))

# Humidity Rules
kb.tell(expr("(LowHumidity(x) & Humidity(x)) ==> Weather(x, Dry)"))
kb.tell(expr("(HighHumidity(x) & Humidity(x)) ==> Weather(x, RainOrThunderstorms)"))

# Barometric Pressure Rules
kb.tell(expr("(RisingPressure(x) & Pressure(x)) ==> Weather(x, Improving)"))
kb.tell(expr("(FallingPressure(x) & Pressure(x)) ==> Weather(x, ApproachingStorms)"))

# built rules
kb.tell(expr(" (Weather(x, Improving) & Weather(x, Dry)) ==> Weather(x, YOU_did_it)"))



def predict_weather(observed_conditions):
    weath = []
    weath2 = []
    for condition in observed_conditions:
        kb.tell(expr(condition))

    result = list(fol_fc_ask(kb, expr("Weather(x, w)")))
    print("Inference result:")
    print(result)

    # Process inferences and generate explanations
    for l in result:
        for key, value in l.items():
            element_value = value
            weath.append(element_value)

    # Format inferred weather predictions
    for i in range(0, len(weath)):
        if i % 2 != 0:
            weath2.append(str(weath[i]))

    return weath2


def show_weather_announcement(weather, explanation):
    announcement_window = tk.Toplevel(root)
    announcement_window.title("Weather Announcement")
    announcement_window.geometry("400x400")
    announcement_window.configure(bg="#0A3258")

    weather_label = tk.Label(announcement_window, text=f"Today's Weather",
                             font=("Poppins", 16, "bold"), bg="#0A3258", fg="#ffffff")
    weather_label.pack()
    weather_label = tk.Label(announcement_window, text=f" {', '.join(weather)}",
                             font=("Poppins", 12), bg="#0A3258", fg="#ffffff")
    weather_label.pack(pady=10)

    explanation_label = tk.Label(announcement_window, text="EXPLANATION",
                                 font=("Poppins", 14, "bold"), bg="#0A3258", fg="#ffffff")
    explanation_label.pack(pady=5)

    explanation_text = tk.Text(announcement_window, font=("Poppins", 12), height=10, wrap=tk.WORD,
                               bg="#09467F", fg="#FFFFFF")
    explanation_text.insert(tk.END, explanation)
    explanation_text.pack(pady=10)

    ok_button = tk.Button(announcement_window, text="OK", command=announcement_window.destroy,
                          font=("Poppins", 12, "bold"), bg="#ffffff", fg="#09467F")
    ok_button.pack(pady=10)


def get_weather_prediction():
    observed_conditions = ['Sky(Today)', 'Wind(Today)', 'Temperature(Today)', 'Humidity(Today)', 'Pressure(Today)']
    for var, (label, value) in variables.items():
        if value.get() == "Yes":
            observed_conditions.append(f"{label}(Today)")
    predicted_weather = predict_weather(observed_conditions)
    explanation = generate_explanation(observed_conditions, predicted_weather)
    show_weather_announcement(predicted_weather, explanation)


def generate_explanation(observed_conditions, predicted_weather):
    print("Observed conditions:", observed_conditions)  # Print observed conditions
    explanation = "The system predicts the following weather conditions using the forward chaining method based on the observed conditions:\n"

    # Detailed explanations for each observed condition
    detailed_explanations = {
        "SkyClear": "Clear skies usually indicate sunny weather.",
        "FewClouds": "A few clouds may lead to partly cloudy conditions.",
        "Overcast": "Overcast skies suggest cloudy weather.",
        "CalmWind": "Calm winds usually indicate stable weather.",
        "GentleBreeze": "A gentle breeze suggests fair weather conditions.",
        "StrongWind": "Strong winds may lead to stormy conditions.",
        "ColdTemp": "Cool temperatures suggest mild weather.",
        "WarmTemp": "Warm temperatures indicate pleasant weather.",
        "HotTemp": "Hot temperatures may lead to a heatwave.",
        "LowHumidity": "Low humidity indicates dry weather.",
        "HighHumidity": "High humidity may lead to rain or thunderstorms.",
        "RisingPressure": "Rising barometric pressure suggests improving weather conditions.",
        "FallingPressure": "Falling barometric pressure may indicate approaching storms."
    }

    # Add detailed explanations for each observed condition
    for condition in observed_conditions:
        condition_parts = condition.split('(')
        condition_type = condition_parts[0].strip()  # Strip any leading/trailing whitespace
        print("Condition type:", condition_type)  # Print condition type
        if condition_type in detailed_explanations:
            explanation += f"\n- {condition_type}: {detailed_explanations[condition_type]}"

    # Add the inferred weather condition to the explanation
    explanation += f"\n\n- Weather: {', '.join(predicted_weather)}"

    return explanation



# Create a tkinter window
root = tk.Tk()
root.title("Weather Prediction")
root.configure(bg="#ffffff")  # Set background color to white

# Dictionary to store variables for each situation
variables = {}


def create_section(root, title, bg_image_path, font_size=12, font_family="Arial", title_color="#F9F9F9"):
    title_font = (font_family, font_size)

    section_frame = tk.LabelFrame(root, text=title, font=title_font, foreground=title_color, bd=0, highlightthickness=0)
    section_frame.grid(sticky="nsew", padx=10, pady=5)

    # Load the image
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Set the background image
    section_frame.config(bg=root.cget('bg'))
    bg_label = tk.Label(section_frame, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)

    return section_frame

def set_root_background(root, image_path):
    image = tk.PhotoImage(file=image_path)
    background_label = tk.Label(root, image=image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.image = image

# Function to create a row for a situation
def create_row(section, label_text, row):
    var = tk.StringVar(value="No")
    check_button = tk.Checkbutton(section, text=label_text, variable=var, onvalue="Yes", offvalue="No",
                                  font=("Arial", 10, "bold"), bg="#09467F", fg="#ffffff",
                                  selectcolor="#0A3258")
    check_button.grid(row=row, column=0, padx=10, pady=5, sticky="w")
    variables[label_text] = (label_text, var)

    if label_text in temperature_ranges:
        temp_label_text = temperature_ranges[label_text]
        temp_label = tk.Label(section, text=temp_label_text, font=("Arial", 10), bg="#09467F", fg="#F9F9F9")
        temp_label.grid(row=row, column=1, padx=10, pady=5)


# Define temperature ranges
temperature_ranges = {
    'ColdTemp': '< 20 C°',
    'WarmTemp': 'between 20o and 30 C°',
    'HotTemp': '> 30 C°',
}

# Create rows for each situation
situations = ['SkyClear', 'FewClouds', 'Overcast', 'CalmWind', 'GentleBreeze', 'StrongWind',
              'ColdTemp', 'WarmTemp', 'HotTemp', 'LowHumidity', 'HighHumidity',
              'RisingPressure', 'FallingPressure']
sky = ['SkyClear', 'FewClouds', 'Overcast']
wind = ['CalmWind', 'GentleBreeze', 'StrongWind']
temp = ['ColdTemp', 'WarmTemp', 'HotTemp']
humidity = ['LowHumidity', 'HighHumidity']
pressure = ['RisingPressure', 'FallingPressure']


set_root_background(root, "Rectangle_13.png")

Sky_situation = create_section(root, "Sky situation", "Rectangle_12.png",font_size=14, font_family="Poppins", title_color="#0A3258")
for i, situation in enumerate(sky):
    create_row(Sky_situation, situation, i)


Wind_situation = create_section(root, "Wind","Rectangle_12.png",font_size=14, font_family="Poppins", title_color="#0A3258")
for i, situation in enumerate(wind):
    create_row(Wind_situation, situation, i)

Temperature_sit = create_section(root, "Temperature","Rectangle_12.png" ,font_size=14, font_family="Poppins", title_color="#0A3258")
for i, situation in enumerate(temp):
    create_row(Temperature_sit, situation, i)

Humidity_sit = create_section(root, "Humidity","Rectangle_12.png" ,font_size=14, font_family="Poppins", title_color="#0A3258")
for i, situation in enumerate(humidity):
    create_row(Humidity_sit, situation, i)


Pressure_sit = create_section(root, "Pressure", "Rectangle_12.png",font_size=14, font_family="Poppins", title_color="#0A3258")
for i, situation in enumerate(pressure):
    create_row(Pressure_sit, situation, i)

# Button to predict weather
predict_button = tk.Button(root, text="Predict Weather", command=get_weather_prediction,
                           font=("Arial", 14, "bold"), bg="#ffffff", fg="#0A3258")  # Dark turquoise background
predict_button.grid(row=len(situations), column=0, columnspan=3, pady=10)

# Label to display the predicted weather
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#ffffff",
                        fg="#333")  # White background and dark text
result_label.grid(row=len(situations) + 1, column=0, columnspan=3)

# Run the tkinter event loop
root.mainloop()