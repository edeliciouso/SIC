import streamlit as st
import os

import random
recipes = []
with open('recipes_formatted.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.split("!")
        recipes.append(line)

def findIngredient(item):
    possibleRecipes = []
    for index, recipe in enumerate(recipes):
        if len(recipe) > 1 and recipe[1].find(item) > 0:  # Check if recipe has at least 2 elements
            possibleRecipes.append(index)
    return possibleRecipes

with st.empty():
    dictItem = os.listdir("detected")
    if len(dictItem) == 1:
        detected = True
        ingredientImage = "detected/" + dictItem[0]
        ingredientTitle = dictItem[0].replace(".png", "")
        possibleRecipes = findIngredient(dictItem[0].replace(".png", ""))

        if (len(possibleRecipes) > 0):
            rand = possibleRecipes[random.randint(0, len(possibleRecipes) - 1)]
            recipeTitle = recipes[rand][0]
            recipeInstructions = "Recipe : \n\n"
            for index, instruction in enumerate(recipes[rand][2].split(".")):
                # Ensure we don't add an empty instruction if there's a trailing period
                if instruction.strip():
                    recipeInstructions = recipeInstructions + str(index + 1) + ". " + instruction.strip() + "\n\n"
        else:
            recipeTitle = "No Recipes"
            recipeInstructions = "Recipe : \n\n None"
    else:
        detected = False
        ingredientImage = "no-image.png"
        ingredientTitle = ""
        recipeTitle = ""
        recipeInstructions = ""

st.title("Shelf-Aware: Recipe Recommendation System Using AI and IoT Fridge Monitoring.")
st.header("Ingredient that was detected:  {}".format(ingredientTitle))
st.image(ingredientImage, width=200)

if (detected):
    st.header("Recipe that Can be Made:")
    st.subheader(recipeTitle)
    st.subheader(recipeInstructions)
    st.button("New Recipe")
else:
    st.rerun()