import json
import streamlit as st

# --- 1. APP CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Offline Recipes", page_icon="📖", initial_sidebar_state="collapsed")

# --- 2. DATA INITIALIZATION ---
if 'recipes' not in st.session_state:
    st.session_state.recipes = [
        {"name": "Beef & Cabbage Skillet", "type": "Entree", "method": "Stovetop", "ingredients": "1lb Ground Beef, 1/2 Cabbage, Butter, Cumin", "instructions": "Brown beef in butter. Add shredded cabbage and cumin. Cook until soft."},
        {"name": "Lemon Shrimp Zucchini", "type": "Entree", "method": "Stovetop", "ingredients": "Shrimp, Zucchini, Lemon, Garlic, Butter", "instructions": "Sauté shrimp in butter. Remove. Toss zucchini with lemon and garlic."},
        {"name": "Garlic Butter Steak & Mushrooms", "type": "Entree", "method": "Stovetop", "ingredients": "Sirloin, Mushrooms, Butter, Garlic", "instructions": "Sear steak in butter. Add mushrooms and garlic. Cook until done."},
        {"name": "Sheet Pan Chicken & Broccoli", "type": "Entree", "method": "Oven", "ingredients": "Chicken, Broccoli, Olive Oil, Paprika", "instructions": "Toss on pan. Bake 425°F for 25 mins."},
        {"name": "Stuffed Zucchini Boats", "type": "Entree", "method": "Oven", "ingredients": "Zucchini, Beef, Marinara, Mozzarella", "instructions": "Hollow zucchini. Fill with cooked beef/sauce. Bake 375°F for 20 mins."},
        {"name": "AF Chili Lime Salmon", "type": "Entree", "method": "Air Fryer", "ingredients": "Salmon, Lime, Chili Powder, Olive Oil", "instructions": "Air fry 400°F for 8 mins."},
        {"name": "Blueberry Overnight Oats", "type": "Breakfast", "method": "Fridge", "ingredients": "Oats, Milk, Blueberries, Honey", "instructions": "Mix in jar. Refrigerate overnight."},
        {"name": "Hard Boiled Egg Pack", "type": "Breakfast", "method": "Fridge", "ingredients": "Eggs, Salt, Apple Slices", "instructions": "Boil eggs ahead. Pack with fruit."},
    ]

if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = 0

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🍳 Offline Recipes")
page = st.sidebar.radio("", ["Home", "Add Recipe", "Shopping List", "Import/Export"])

if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

# --- 4. HOME PAGE ---
if st.session_state.page == "Home":
    st.title("📖 My Recipes")
    
    # Filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search recipes").lower()
    with col2:
        cat_filter = st.selectbox("Category", ["All", "Entree", "Breakfast", "Sides"])
    
    # Filter logic
    recipes_df = st.session_state.recipes
    if cat_filter != "All":
        recipes_df = [r for r in recipes_df if r["type"] == cat_filter]
    if search:
        recipes_df = [r for r in recipes_df if search in r["name"].lower()]
    
    recipes_df = sorted(recipes_df, key=lambda x: x["name"])
    
    # Display recipes as grid
    if recipes_df:
        cols = st.columns(2)
        for idx, recipe in enumerate(recipes_df):
            with cols[idx % 2]:
                with st.container(border=True):
                    st.subheader(recipe["name"])
                    st.caption(f"🏷️ {recipe['type']} • ⚙️ {recipe['method']}")
                    if st.button("View", key=f"view_{idx}", use_container_width=True):
                        st.session_state.selected_idx = st.session_state.recipes.index(recipe)
                        st.session_state.page = "Detail"
                        st.rerun()
    else:
        st.info("No recipes found. Add one to get started!")

# --- 5. DETAIL PAGE ---
if st.session_state.page == "Detail":
    recipe = st.session_state.recipes[st.session_state.selected_idx]
    st.title(recipe["name"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Ingredients")
        st.info(recipe["ingredients"])
        if st.button("🛒 Add to Shopping List", use_container_width=True):
            st.session_state.shopping_list.append(f"{recipe['name']}: {recipe['ingredients']}")
            st.success("Added to list!")
    
    with col2:
        st.subheader("👨‍🍳 Instructions")
        st.write(recipe["instructions"])
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Back", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with col2:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.page = "Edit"
            st.rerun()
    with col3:
        if st.button("🗑️ Delete", type="secondary", use_container_width=True):
            st.session_state.recipes.pop(st.session_state.selected_idx)
            st.session_state.page = "Home"
            st.rerun()

# --- 6. EDIT PAGE ---
elif st.session_state.page == "Edit":
    recipe = st.session_state.recipes[st.session_state.selected_idx]
    st.title("✏️ Edit Recipe")
    
    with st.form("edit_form"):
        name = st.text_input("Recipe Name", recipe["name"])
        recipe_type = st.selectbox("Type", ["Entree", "Breakfast", "Sides"], index=["Entree", "Breakfast", "Sides"].index(recipe["type"]))
        method = st.selectbox("Method", ["Stovetop", "Oven", "Air Fryer", "Fridge"], index=["Stovetop", "Oven", "Air Fryer", "Fridge"].index(recipe["method"]))
        ingredients = st.text_area("Ingredients", recipe["ingredients"])
        instructions = st.text_area("Instructions", recipe["instructions"])
        
        if st.form_submit_button("Save Changes"):
            st.session_state.recipes[st.session_state.selected_idx] = {
                "name": name,
                "type": recipe_type,
                "method": method,
                "ingredients": ingredients,
                "instructions": instructions
            }
            st.session_state.page = "Home"
            st.rerun()
    
    if st.button("Cancel"):
        st.session_state.page = "Home"
        st.rerun()

# --- 7. ADD RECIPE PAGE ---
elif st.session_state.page == "Add Recipe":
    st.title("➕ Add New Recipe")
    
    with st.form("add_form"):
        name = st.text_input("Recipe Name")
        recipe_type = st.selectbox("Type", ["Entree", "Breakfast", "Sides"])
        method = st.selectbox("Method", ["Stovetop", "Oven", "Air Fryer", "Fridge"])
        ingredients = st.text_area("Ingredients (comma-separated)")
        instructions = st.text_area("Instructions")
        
        if st.form_submit_button("Create Recipe"):
            if name and ingredients and instructions:
                st.session_state.recipes.append({
                    "name": name,
                    "type": recipe_type,
                    "method": method,
                    "ingredients": ingredients,
                    "instructions": instructions
                })
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Please fill all fields!")
    
    if st.button("Cancel"):
        st.session_state.page = "Home"
        st.rerun()

# --- 8. SHOPPING LIST PAGE ---
elif st.session_state.page == "Shopping List":
    st.title("🛒 Shopping List")
    
    if st.session_state.shopping_list:
        for i, item in enumerate(st.session_state.shopping_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {item}")
            with col2:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.shopping_list.pop(i)
                    st.rerun()
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy All", use_container_width=True):
                text = "\n".join(st.session_state.shopping_list)
                st.code(text, language="text")
        with col2:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.shopping_list = []
                st.rerun()
    else:
        st.info("Your shopping list is empty. Add ingredients from recipes!")
    
    if st.button("Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

# --- 9. IMPORT/EXPORT PAGE ---
elif st.session_state.page == "Import/Export":
    st.title("📤 Import/Export Recipes")
    
    # Export section
    st.subheader("📥 Export Your Recipes")
    st.write("Download all recipes as JSON to backup or transfer to another device:")
    
    recipes_json = json.dumps(st.session_state.recipes, indent=2)
    st.download_button(
        label="⬇️ Download Recipes (JSON)",
        data=recipes_json,
        file_name="recipes_backup.json",
        mime="application/json"
    )
    
    st.markdown("---")
    
    # Import section
    st.subheader("📤 Import Recipes")
    st.write("Upload a JSON file to add recipes:")
    
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    if uploaded_file is not None:
        try:
            imported_recipes = json.load(uploaded_file)
            if isinstance(imported_recipes, list):
                st.session_state.recipes.extend(imported_recipes)
                st.success(f"✅ Imported {len(imported_recipes)} recipe(s)!")
                st.rerun()
            else:
                st.error("Invalid JSON format. Expected a list of recipes.")
        except Exception as e:
            st.error(f"Error importing file: {e}")

