import streamlit as st
import json
from datetime import datetime

# Adicione esta verificação para importação condicional do career_agent
try:
    from career_agent import CareerDevelopmentAgent
    career_agent_available = True
except ImportError as e:
    st.error(f"Erro ao importar CareerDevelopmentAgent: {str(e)}")
    career_agent_available = False
except Exception as e:
    st.error(f"Erro inesperado: {str(e)}")
    career_agent_available = False

# ... (o restante do código permanece igual)

if submitted:
    if not all([current_skills, career_goals]):
        st.error("Por favor, preencha os campos obrigatórios (*)")
    else:
        with st.spinner("Analisando seu perfil e criando plano personalizado..."):
            user_profile = {
                "current_skills": [s.strip() for s in current_skills.split(",")],
                "years_experience": years_experience,
                "industry": industry,
                "career_goals": [g.strip() for g in career_goals.split(",")],
                "learning_preferences": learning_preferences,
                "time_commitment": time_commitment,
                "additional_info": additional_info,
                "timestamp": datetime.now().isoformat()
            }
            
            try:
                # Inicializar o agente com a chave API
                agent = CareerDevelopmentAgent(api_key=st.secrets.get("GEMINI_API_KEY"))
                career_plan = agent.analyze_profile(user_profile)
                
                st.markdown('<h2 class="section-header">📋 Seu Plano de Desenvolvimento</h2>', unsafe_allow_html=True)
                st.markdown(career_plan)
                
                # ... (o restante do código permanece igual)
            
            except Exception as e:
                st.error(f"Erro ao gerar plano: {str(e)}")
                if debug_mode:
                    st.exception(e)