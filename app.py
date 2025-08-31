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

st.set_page_config(
    page_title="Career Development Agent", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"  # Garante que a sidebar seja expandida por padrão
)

# CSS customizado - simplificado para evitar problemas
st.markdown("""
<style>
.main-header { 
    font-size: 2.5rem; 
    color: #1f77b4; 
    text-align: center; 
    margin-bottom: 2rem; 
}
.section-header { 
    font-size: 1.8rem; 
    color: #2c3e50; 
    margin-top: 2rem; 
    margin-bottom: 1rem; 
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🎯 Career Development Agent</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Sobre")
    st.info("Este agente ajuda você a criar um plano personalizado para alcançar seus objetivos de carreira.")
    debug_mode = st.checkbox("Modo Debug", value=False)
    
    # Adicione informações de status
    st.header("Status do Sistema")
    if career_agent_available:
        st.success("Career Agent: Disponível")
    else:
        st.error("Career Agent: Indisponível")

# Verifique se o career_agent está disponível antes de renderizar o formulário
if not career_agent_available:
    st.warning("""
    O módulo CareerDevelopmentAgent não está disponível. 
    Por favor, verifique se o arquivo `career_agent.py` existe no mesmo diretório.
    """)
    
    # Mostre instruções de exemplo para criar o arquivo career_agent.py
    with st.expander("Como criar o arquivo career_agent.py"):
        st.code("""
# career_agent.py - Exemplo mínimo
class CareerDevelopmentAgent:
    def __init__(self):
        pass
    
    def analyze_profile(self, user_profile):
        return '''
        # Plano de Desenvolvimento de Carreira (Exemplo)
        
        ## Análise de Perfil
        Com base nas suas habilidades atuais: {skills}
        e seus objetivos: {goals}
        
        ## Recomendações
        1. Curso de Python Avançado
        2. Especialização em {goal}
        3. Projetos práticos na área
        
        ## Timeline Estimada
        - 3-6 meses para transição básica
        - 6-12 meses para especialização
        '''.format(
            skills=', '.join(user_profile.get('current_skills', [])),
            goals=', '.join(user_profile.get('career_goals', [])),
            goal=user_profile.get('career_goals', [''])[0]
        )
        """, language="python")
else:
    # Formulário principal - só é exibido se o career_agent estiver disponível
    with st.form("career_form"):
        st.markdown('<h2 class="section-header">Seu Perfil Profissional</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_skills = st.text_area(
                "Habilidades Atuais*", 
                placeholder="Python, Data Analysis, Project Management...",
                help="Liste suas habilidades separadas por vírgula"
            )
            years_experience = st.slider("Anos de Experiência Profissional*", 0, 30, 3)
            industry = st.selectbox("Setor/Indústria*", ["Technology", "Healthcare", "Finance", "Education", "Marketing", "Other"])
        
        with col2:
            career_goals = st.text_area(
                "Objetivos de Carreira*", 
                placeholder="Data Scientist, AI Engineer, Product Manager...",
                help="Liste seus objetivos de carreira separados por vírgula"
            )
            learning_preferences = st.multiselect(
                "Preferências de Aprendizado*", 
                ["Video courses", "Reading", "Hands-on projects", "Formal courses", "Mentoring"], 
                default=["Video courses", "Hands-on projects"]
            )
            time_commitment = st.selectbox("Disponibilidade Semanal*", ["5-10 hours", "10-15 hours", "15-20 hours", "20+ hours"])
        
        additional_info = st.text_area(
            "Contexto Adicional", 
            placeholder="Experiências relevantes, conquistas, desafios...",
            help="Informações adicionais que possam ajudar na análise"
        )
        
        submitted = st.form_submit_button("🚀 Gerar Plano de Desenvolvimento")

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
                    agent = CareerDevelopmentAgent()
                    career_plan = agent.analyze_profile(user_profile)
                    
                    st.markdown('<h2 class="section-header">📋 Seu Plano de Desenvolvimento</h2>', unsafe_allow_html=True)
                    st.markdown(career_plan)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download do Plano (JSON)", 
                            data=json.dumps(user_profile, indent=2, ensure_ascii=False), 
                            file_name="career_plan.json", 
                            mime="application/json"
                        )
                    with col2:
                        st.download_button(
                            "📥 Download do Plano (TXT)", 
                            data=career_plan, 
                            file_name="career_plan.txt", 
                            mime="text/plain"
                        )
                
                except Exception as e:
                    st.error(f"Erro ao gerar plano: {str(e)}")
                    if debug_mode:
                        st.exception(e)

st.markdown("---")
st.caption("Career Development Agent v1.0 | Desenvolvido com Agno Framework")