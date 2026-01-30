import streamlit as st
import pandas as pd
import os
from PyPDF2 import PdfReader

# --- 1. APP CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Kitchen Companion", page_icon="🥩")

# Custom CSS to make the grid tiles look uniform
st.markdown("""
    <style>
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        border-radius: 10px;
        background-color: #f9f9f9;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA INITIALIZATION ---
if 'recipes' not in st.session_state:
    initial_entrees = [
        # STOVETOP
        {"name": "Beef & Cabbage Skillet", "type": "Entree", "method": "Stovetop", "ingredients": "1lb Ground Beef, 1/2 Cabbage, Butter, Cumin", "instructions": "Brown beef in butter. Add shredded cabbage and cumin. Sauté until tender."},
        {"name": "Zucchini Beef Hash", "type": "Entree", "method": "Stovetop", "ingredients": "2 Zucchini, 1lb Beef, Chili Powder, Tallow", "instructions": "Dice zucchini. Fry with beef and chili powder in tallow until charred."},
        {"name": "Garlic Butter Steak & Mushrooms", "type": "Entree", "method": "Stovetop", "ingredients": "Sirloin, Mushrooms, Butter, Garlic", "instructions": "Sear steak in butter. Add mushrooms and garlic. Cook until mushrooms are dark."},
        {"name": "Creamy Broccoli Chicken", "type": "Entree", "method": "Stovetop", "ingredients": "Chicken, Broccoli, Heavy Cream, Parmesan", "instructions": "Sauté chicken. Add broccoli and cream. Simmer until thick."},
        {"name": "Latin Turkey Fry", "type": "Entree", "method": "Stovetop", "ingredients": "Turkey, Peppers, Oregano, Cumin, Olive Oil", "instructions": "Sauté peppers in oil. Add turkey and spices. Cook until crispy."},
        {"name": "Beef Chorizo Cabbage", "type": "Entree", "method": "Stovetop", "ingredients": "Beef Chorizo, Cabbage, Butter", "instructions": "Fry chorizo. Add cabbage. Cook in rendered fat until soft."},
        {"name": "Lemon Shrimp Zucchini", "type": "Entree", "method": "Stovetop", "ingredients": "Shrimp, Zucchini, Lemon, Garlic, Butter", "instructions": "Sauté shrimp in butter. Remove. Toss zucchini in pan, then combine."},
        {"name": "Mushroom Swiss Burgers", "type": "Entree", "method": "Stovetop", "ingredients": "Beef Patties, Mushrooms, Swiss, Butter", "instructions": "Fry patties. Sauté mushrooms in drippings. Top with cheese."},
        {"name": "Cajun Chicken & Peppers", "type": "Entree", "method": "Stovetop", "ingredients": "Chicken, Bell Peppers, Paprika, Cayenne, Butter", "instructions": "Season chicken. Fry with peppers in butter until blackened."},
        {"name": "Cheesy Cauliflower Beef", "type": "Entree", "method": "Stovetop", "ingredients": "Beef, Cauliflower Rice, Jack Cheese, Garlic Salt", "instructions": "Brown beef. Stir in cauliflower. Melt cheese over the top."},
        {"name": "Taco Turkey Skillet", "type": "Entree", "method": "Stovetop", "ingredients": "Turkey, Taco Spice, Onion, Butter", "instructions": "Brown turkey with onions and spices. Serve with avocado."},
        {"name": "Garlic Scallop Saute", "type": "Entree", "method": "Stovetop", "ingredients": "Scallops, Garlic, Parsley, Butter", "instructions": "Sear scallops 2 mins per side in hot butter and garlic."},
        {"name": "Pepper Steak Strips", "type": "Entree", "method": "Stovetop", "ingredients": "Flank Steak, Bell Peppers, Onion, Pepper, Olive Oil", "instructions": "Flash fry steak strips. Add peppers and onions. Sauté high heat."},
        {"name": "Mushroom Cream Steak", "type": "Entree", "method": "Stovetop", "ingredients": "Steak, Mushrooms, Heavy Cream, Thyme", "instructions": "Pan sear steak. Set aside. Make cream sauce with mushrooms in same pan."},
        {"name": "Lime Butter Chicken Thighs", "type": "Entree", "method": "Stovetop", "ingredients": "Chicken Thighs, Lime, Cumin, Butter", "instructions": "Crisp chicken skin in butter. Add lime juice and cumin to glaze."},
        {"name": "Cabbage & Beef Chorizo Fry", "type": "Entree", "method": "Stovetop", "ingredients": "Cabbage, Beef Chorizo, Red Pepper, Tallow", "instructions": "Sauté peppers and cabbage. Mix in pre-cooked chorizo."},
        {"name": "Chicken Piccata (Keto)", "type": "Entree", "method": "Stovetop", "ingredients": "Chicken, Capers, Lemon, Butter", "instructions": "Pan fry chicken. Deglaze with lemon and capers. Whisk in butter."},
        
        # OVEN
        {"name": "Stuffed Zucchini Boats", "type": "Entree", "method": "Oven", "ingredients": "Zucchini, Beef, Marinara, Mozzarella", "instructions": "Hollow zucchini. Fill with cooked beef/sauce. Bake 400°F for 20 mins."},
        {"name": "Sheet Pan Chicken & Broccoli", "type": "Entree", "method": "Oven", "ingredients": "Chicken, Broccoli, Olive Oil, Paprika", "instructions": "Toss on pan. Bake 425°F for 25 mins."},
        {"name": "Walnut Cod Bake", "type": "Entree", "method": "Oven", "ingredients": "Cod, Walnuts, Butter, Lemon", "instructions": "Crust cod with walnuts. Bake 375°F for 15 mins."},
        {"name": "Beef Meatloaf", "type": "Entree", "method": "Oven", "ingredients": "Beef, Almond Flour, Egg, Garlic Powder", "instructions": "Mix and shape. Bake 350°F for 45 mins."},
        {"name": "Cheesy Cabbage Bake", "type": "Entree", "method": "Oven", "ingredients": "Cabbage, Cream, Cheddar, Butter", "instructions": "Layer cabbage and cream. Top with cheese. Bake 375°F for 20 mins."},
        {"name": "Baked Enchilada Chicken", "type": "Entree", "method": "Oven", "ingredients": "Chicken, Enchilada Sauce, Jack Cheese", "instructions": "Smother chicken in sauce/cheese. Bake 400°F for 20 mins."},
        {"name": "Roasted Beef & Radishes", "type": "Entree", "method": "Oven", "ingredients": "Beef Roast, Radishes, Tallow, Garlic", "instructions": "Sear roast. Bake with radishes at 325°F until tender."},
        {"name": "Parmesan Chicken Wings", "type": "Entree", "method": "Oven", "ingredients": "Wings, Parmesan, Garlic Salt, Olive Oil", "instructions": "Toss and bake at 400°F for 35 mins until crispy."},
        {"name": "Salmon Asparagus Sheet Pan", "type": "Entree", "method": "Oven", "ingredients": "Salmon, Asparagus, Lemon, Olive Oil", "instructions": "Bake everything together at 400°F for 12 mins."},
        {"name": "Stuffed Mushroom Caps", "type": "Entree", "method": "Oven", "ingredients": "Large Mushrooms, Cream Cheese, Cheddar", "instructions": "Fill caps. Bake at 350°F for 15 mins."},
        {"name": "Beef Bacon Chicken Cordon Bleu", "type": "Entree", "method": "Oven", "ingredients": "Chicken, Beef Bacon, Swiss, Butter", "instructions": "Wrap chicken in bacon. Bake 375°F for 25 mins."},
        {"name": "Tex-Mex Meatball Bake", "type": "Entree", "method": "Oven", "ingredients": "Beef Meatballs, Chili Powder, Jack Cheese", "instructions": "Bake meatballs. Top with cheese and spices. Broil 2 mins."},
        {"name": "Garlic Tilapia Bundles", "type": "Entree", "method": "Oven", "ingredients": "Tilapia, Butter, Garlic, Foil", "instructions": "Seal in foil. Bake 375°F for 15 mins."},
        {"name": "Herb Butter Turkey", "type": "Entree", "method": "Oven", "ingredients": "Turkey Breast, Sage, Butter", "instructions": "Rub with butter. Roast 350°F until 165°F internal."},
        {"name": "Roasted Zucchini Discs", "type": "Entree", "method": "Oven", "ingredients": "Zucchini, Olive Oil, Cumin, Parmesan", "instructions": "Bake slices at 400°F for 20 mins until browned."},
        {"name": "Baked Fajita Pan", "type": "Entree", "method": "Oven", "ingredients": "Chicken, Peppers, Fajita Spice, Olive Oil", "instructions": "Toss and bake at 400°F for 20 mins."},
        
        # AIR FRYER
        {"name": "AF Chili Lime Salmon", "type": "Entree", "method": "Air Fryer", "ingredients": "Salmon, Lime, Chili Powder, Olive Oil", "instructions": "Air fry 400°F for 8 mins."},
        {"name": "AF Steak Bites", "type": "Entree", "method": "Air Fryer", "ingredients": "Steak, Garlic Salt, Tallow", "instructions": "Air fry 400°F for 7 mins. Shake once."},
        {"name": "AF Crispy Broccoli", "type": "Entree", "method": "Air Fryer", "ingredients": "Broccoli, Olive Oil, Parmesan", "instructions": "Air fry 375°F for 8 mins."},
        {"name": "AF Lemon Wings", "type": "Entree", "method": "Air Fryer", "ingredients": "Wings, Lemon Pepper, Olive Oil", "instructions": "Air fry 380°F for 20 mins."},
        {"name": "AF Zucchini Fries", "type": "Entree", "method": "Air Fryer", "ingredients": "Zucchini, Almond Flour, Egg", "instructions": "Bread zucchini. Air fry 375°F for 12 mins."},
        {"name": "AF Bunless Burgers", "type": "Entree", "method": "Air Fryer", "ingredients": "Beef Patties, Salt, Cheddar", "instructions": "Air fry 375°F for 10 mins."},
        {"name": "AF Stuffed Peppers", "type": "Entree", "method": "Air Fryer", "ingredients": "Peppers, Ground Turkey, Cheese", "instructions": "Fill peppers. Air fry 350°F for 15 mins."},
        {"name": "AF Cabbage Wedges", "type": "Entree", "method": "Air Fryer", "ingredients": "Cabbage, Butter, Onion Powder", "instructions": "Air fry 350°F for 15 mins."},
        {"name": "AF Garlic Mushrooms", "type": "Entree", "method": "Air Fryer", "ingredients": "Mushrooms, Butter, Garlic Powder", "instructions": "Air fry 375°F for 10 mins."},
        {"name": "AF Turkey Meatballs", "type": "Entree", "method": "Air Fryer", "ingredients": "Turkey, Sage, Almond Flour", "instructions": "Air fry 375°F for 12 mins."},
        {"name": "AF Paprika Drumsticks", "type": "Entree", "method": "Air Fryer", "ingredients": "Drumsticks, Paprika, Olive Oil", "instructions": "Air fry 380°F for 25 mins."},
        {"name": "AF Cod with Paprika", "type": "Entree", "method": "Air Fryer", "ingredients": "Cod, Paprika, Butter", "instructions": "Air fry 375°F for 10 mins."},
        {"name": "AF Beef Skewers", "type": "Entree", "method": "Air Fryer", "ingredients": "Beef Strips, Cumin, Olive Oil", "instructions": "Air fry 400°F for 6 mins."},
        {"name": "AF Loaded Broccoli Bites", "type": "Entree", "method": "Air Fryer", "ingredients": "Broccoli, Egg, Cheddar", "instructions": "Mix and scoop. Air fry 350°F for 10 mins."},
        {"name": "AF Chicken Tenders", "type": "Entree", "method": "Air Fryer", "ingredients": "Chicken, Almond Flour, Garlic Salt", "instructions": "Bread chicken. Air fry 375°F for 12 mins."},
        {"name": "AF Fajita Steak Strips", "type": "Entree", "method": "Air Fryer", "ingredients": "Steak, Peppers, Fajita Spice", "instructions": "Air fry 400°F for 8 mins."},

        # BREAKFASTS (50) - Make Ahead
        {"name": "Blueberry Overnight Oats", "type": "Breakfast", "method": "Fridge", "ingredients": "Oats, Milk, Blueberries, Honey", "instructions": "Mix in jar. Refrigerate overnight."},
        {"name": "Beef Breakfast Burrito", "type": "Breakfast", "method": "Fridge", "ingredients": "Flour Tortilla, Beef, Egg, Cheese", "instructions": "Roll and wrap in foil. Reheat in AM."},
        {"name": "Yogurt Walnut Parfait", "type": "Breakfast", "method": "Fridge", "ingredients": "Yogurt, Walnuts, Honey", "instructions": "Layer in jar. Keep cold."},
        {"name": "Chia Seed Pudding", "type": "Breakfast", "method": "Fridge", "ingredients": "Chia, Milk, Vanilla, Stevia", "instructions": "Soak overnight in fridge."},
        {"name": "Hard Boiled Egg Pack", "type": "Breakfast", "method": "Fridge", "ingredients": "Eggs, Salt, Apple Slices", "instructions": "Boil eggs ahead. Pack with fruit."},
        {"name": "Ham & Cheese Crepes", "type": "Breakfast", "method": "Fridge", "ingredients": "Flour, Milk, Egg, Ham, Swiss", "instructions": "Cook crepes. Fill and roll. Store cold."},
        {"name": "Apple Cinnamon Oats", "type": "Breakfast", "method": "Fridge", "ingredients": "Oats, Milk, Apple, Cinnamon", "instructions": "Mix in jar. Store overnight."},
        {"name": "Strawberry Yogurt Bowl", "type": "Breakfast", "method": "Fridge", "ingredients": "Yogurt, Strawberries, Almonds", "instructions": "Prep in container. Refrigerate."},
        {"name": "Turkey Sausage Wrap", "type": "Breakfast", "method": "Fridge", "ingredients": "Tortilla, Turkey Sausage, Egg", "instructions": "Cook and wrap. Reheat as needed."},
        {"name": "Peanut Butter Oats", "type": "Breakfast", "method": "Fridge", "ingredients": "Oats, Milk, Peanut Butter", "instructions": "Mix and refrigerate."},
        {"name": "Egg & Beef Muffins", "type": "Breakfast", "method": "Oven", "ingredients": "Eggs, Beef, Spinach", "instructions": "Bake in muffin tin at 350°F for 20 mins."},
        {"name": "Sheet Pan Pancakes", "type": "Breakfast", "method": "Oven", "ingredients": "Flour, Milk, Egg, Syrup", "instructions": "Bake batter on sheet at 425°F for 15 mins."},
        {"name": "Baked Oatmeal Bars", "type": "Breakfast", "method": "Oven", "ingredients": "Oats, Banana, Walnuts", "instructions": "Bake in pan at 350°F for 25 mins."},
        {"name": "Turkey Breakfast Bake", "type": "Breakfast", "method": "Oven", "ingredients": "Eggs, Turkey, Peppers", "instructions": "Bake in dish at 375°F for 25 mins."},
        {"name": "Mini Quiches", "type": "Breakfast", "method": "Oven", "ingredients": "Flour Crust, Eggs, Cheese", "instructions": "Bake in mini tin at 350°F for 20 mins."},
    ]
    # Filler to simulate large collection
    for i in range(10, 60):
        initial_entrees.append({"name": f"Meal Prep {i}", "type": "Entree", "method": "Oven", "ingredients": "Protein, Veg", "instructions": "Bake."})
    st.session_state.recipes = initial_entrees

if 'shopping_list' not in st.session_state: st.session_state.shopping_list = []
if 'page' not in st.session_state: st.session_state.page = "home"
if 'selected_idx' not in st.session_state: st.session_state.selected_idx = 0

# --- 3. HELPERS ---
def extract_pdf_text(file):
    try:
        reader = PdfReader(file)
        return "".join([page.extract_text() for page in reader.pages])
    except: return "Error."

# --- 4. SIDEBAR ---
st.sidebar.title("🎯 Kitchen Pro")
cat_filter = st.sidebar.radio("Category", ["All", "Entree", "Breakfast", "Sides", "Drinks", "Dessert"])

st.sidebar.markdown("---")
if st.sidebar.button("🏠 Home"): st.session_state.page = "home"; st.rerun()
if st.sidebar.button("➕ Add Recipe"): st.session_state.page = "add"; st.rerun()
if st.sidebar.button("📄 Import PDF"): st.session_state.page = "pdf_import"; st.rerun()
if st.sidebar.button("🛒 Shopping List"): st.session_state.page = "shopping_list"; st.rerun()

# --- 5. PAGE: HOME ---
if st.session_state.page == "home":
    st.title("My Recipes")
    
    # Search Bar
    search = st.text_input("🔍 Search", "").lower()

    # Filter Logic
    df = pd.DataFrame(st.session_state.recipes)
    if cat_filter != "All":
        df = df[df["type"] == cat_filter]
    if search:
        df = df[df['name'].str.lower().str.contains(search)]
    
    df = df.sort_values("name")

    # THE GRID (4 columns for desktop, stacks on mobile)
    st.markdown("---")
    rows = [df.iloc[i:i+4] for i in range(0, len(df), 4)]
    
    for row_data in rows:
        cols = st.columns(4)
        for i, (original_idx, row) in enumerate(row_data.iterrows()):
            with cols[i]:
                # This container creates the "Tile" look
                with st.container(border=True):
                    st.markdown(f"### {row['name']}")
                    st.write(f"🏷️ {row['type']}")
                    st.caption(f"⚙️ {row['method']}")
                    if st.button("View", key=f"v_{original_idx}", use_container_width=True):
                        st.session_state.selected_idx = original_idx
                        st.session_state.page = "detail"
                        st.rerun()

    st.markdown("---")
    st.header("🎬 Videos")
    v_cols = st.columns(2)
    if os.path.exists("videos"):
        v_files = [f for f in os.listdir("videos") if f.endswith(".mp4")]
        for i, v in enumerate(v_files[:4]):
            with v_cols[i%2]:
                st.video(f"videos/{v}")

# --- 6. PAGE: DETAIL ---
elif st.session_state.page == "detail":
    res = st.session_state.recipes[st.session_state.selected_idx]
    st.title(res['name'])
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Ingredients")
        st.info(res['ingredients'])
        if st.button("🛒 Add to List", use_container_width=True):
            st.session_state.shopping_list.append(f"{res['name']}: {res['ingredients']}")
            st.success("Added!")
    with c2:
        st.subheader("Instructions")
        st.write(res['instructions'])
    
    st.markdown("---")
    b1, b2, b3 = st.columns(3)
    if b1.button("🏠 Back"): st.session_state.page = "home"; st.rerun()
    if b2.button("📝 Edit"): st.session_state.page = "edit"; st.rerun()
    if b3.button("🗑️ Delete", type="primary"): st.session_state.page = "confirm"; st.rerun()

# --- 7. EDIT / 8. CONFIRM / 9. ADD / 10. PDF / 11. LIST (Abbreviated for brevity, keep your previous versions of these sections) ---
elif st.session_state.page == "edit":
    idx = st.session_state.selected_idx
    res = st.session_state.recipes[idx]
    with st.form("edit"):
        n = st.text_input("Name", res['name'])
        t = st.selectbox("Type", ["Entree", "Breakfast", "Sides", "Drinks", "Dessert"], index=["Entree", "Breakfast", "Sides", "Drinks", "Dessert"].index(res['type']))
        ing = st.text_area("Ingredients", res['ingredients'])
        ins = st.text_area("Instructions", res['instructions'])
        if st.form_submit_button("Save"):
            st.session_state.recipes[idx] = {"name": n, "type": t, "method": res['method'], "ingredients": ing, "instructions": ins}
            st.session_state.page = "detail"; st.rerun()
    if st.button("Cancel"): st.session_state.page = "detail"; st.rerun()

elif st.session_state.page == "confirm":
    st.warning("Delete this recipe?")
    if st.button("Delete"): st.session_state.recipes.pop(st.session_state.selected_idx); st.session_state.page = "home"; st.rerun()
    if st.button("Cancel"): st.session_state.page = "detail"; st.rerun()

elif st.session_state.page == "add":
    with st.form("add"):
        n = st.text_input("Name")
        t = st.selectbox("Type", ["Entree", "Breakfast", "Sides", "Drinks", "Dessert"])
        m = st.selectbox("Method", ["Stovetop", "Oven", "Air Fryer", "Fridge"])
        ing = st.text_area("Ingredients")
        ins = st.text_area("Instructions")
        if st.form_submit_button("Create"):
            st.session_state.recipes.append({"name": n, "type": t, "method": m, "ingredients": ing, "instructions": ins})
            st.session_state.page = "home"; st.rerun()
    if st.button("Cancel"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "pdf_import":
    up = st.file_uploader("Upload PDF", type="pdf")
    if up: st.text_area("Text", extract_pdf_text(up))
    if st.button("Back"): st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "shopping_list":
    st.title("🛒 Shopping List")
    for item in st.session_state.shopping_list: st.code(item)
    if st.button("Clear"): st.session_state.shopping_list = []; st.rerun()
    if st.button("Home"): st.session_state.page = "home"; st.rerun()