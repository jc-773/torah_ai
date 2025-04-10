import query_embeddings as qe
import streamlit as st



query_to_torah = st.chat_input("Ask me a question about the Torah")
if query_to_torah:
  with st.spinner("Thinking... 🧠"):
      result = qe.vector_search_query(query_to_torah)
      print(f"result--", result)
      similar_verses = qe.search_similar_verses(result)
      print(f"similar_verses--", similar_verses)
      build_prompt = qe.build_prompt(similar_verses, query_to_torah)
      print(f"build_prompt--", build_prompt)
      response = qe.ask_openai(build_prompt)
      print(f"response--", response)
      st.write(response)