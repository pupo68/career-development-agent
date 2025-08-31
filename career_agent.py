import json
import os
import google.generativeai as genai
from datetime import datetime
import streamlit as st

class CareerDevelopmentAgent:
    def __init__(self):
        # Obter a chave API do Gemini dos segredos do Streamlit
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except (KeyError, AttributeError):
            # Fallback para variável de ambiente (desenvolvimento local)
            api_key = os.getenv("GEMINI_API_KEY")
            
        if not api_key:
            st.error("Chave API do Gemini não encontrada. Configure GEMINI_API_KEY nos segredos do Streamlit.")
            raise ValueError("GEMINI_API_KEY não configurada")
        
        # Configurar a API do Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self):
        """Carrega todos os arquivos de conhecimento da pasta career_knowledge"""
        knowledge = {}
        knowledge_dir = "career_knowledge"
        
        # Lista de arquivos para carregar
        knowledge_files = {
            "trends": "trends.json",
            "learning_paths": "learning_paths.json",
            "salary_data": "salary_data.json",
            "certifications": "certifications.json"
        }
        
        for key, filename in knowledge_files.items():
            filepath = os.path.join(knowledge_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    knowledge[key] = json.load(f)
            except FileNotFoundError:
                st.warning(f"Arquivo {filename} não encontrado em {knowledge_dir}")
                knowledge[key] = {}
            except json.JSONDecodeError:
                st.error(f"Erro ao decodificar JSON do arquivo {filename}")
                knowledge[key] = {}
        
        return knowledge
    
    def analyze_profile(self, user_profile):
        """Analisa o perfil do usuário e gera um plano de desenvolvimento de carreira usando Gemini"""
        # Construir o prompt com base no perfil e no conhecimento
        prompt = self._build_prompt(user_profile)
        
        try:
            # Configurar parâmetros de geração
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Gerar resposta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=False
            )
            
            return response.text
            
        except Exception as e:
            return f"Erro ao gerar plano: {str(e)}\n\nPlano alternativo:\n{self._generate_fallback_plan(user_profile)}"
    
    def _build_prompt(self, user_profile):
        """Constroi o prompt para o Gemini com base no perfil do usuário e no conhecimento"""
        # Extrai informações do perfil do usuário
        current_skills = user_profile.get('current_skills', [])
        career_goals = user_profile.get('career_goals', [])
        industry = user_profile.get('industry', '')
        years_experience = user_profile.get('years_experience', 0)
        learning_preferences = user_profile.get('learning_preferences', [])
        time_commitment = user_profile.get('time_commitment', '')
        additional_info = user_profile.get('additional_info', '')
        
        # Formatar o conhecimento para incluir no prompt
        trends_str = json.dumps(self.knowledge.get('trends', {}), ensure_ascii=False, indent=2)
        learning_paths_str = json.dumps(self.knowledge.get('learning_paths', {}), ensure_ascii=False, indent=2)
        salary_data_str = json.dumps(self.knowledge.get('salary_data', {}), ensure_ascii=False, indent=2)
        certifications_str = json.dumps(self.knowledge.get('certifications', {}), ensure_ascii=False, indent=2)
        
        # Construir o prompt
        prompt = f"""
        Você é um consultor de carreira especializado. Sua missão é ajudar profissionais a alcançarem seus objetivos.

        Com base nas informações do usuário abaixo e no conhecimento da base de dados, crie um plano de desenvolvimento de carreira detalhado.

        PERFIL DO USUÁRIO:
        - Habilidades atuais: {current_skills}
        - Objetivos de carreira: {career_goals}
        - Setor/Indústria: {industry}
        - Anos de experiência: {years_experience}
        - Preferências de aprendizado: {learning_preferences}
        - Disponibilidade semanal: {time_commitment}
        - Informações adicionais: {additional_info}

        BASE DE CONHECIMENTO (use essas informações para enriquecer sua análise):
        
        === TENDÊNCIAS DO MERCADO ===
        {trends_str}
        
        === CAMINHOS DE APRENDIZADO ===
        {learning_paths_str}
        
        === DADOS SALARIAIS ===
        {salary_data_str}
        
        === CERTIFICAÇÕES ===
        {certifications_str}

        FORMATO DE RESPOSTA:
        - Use markdown para organização
        - Divida em seções claras: Análise de Perfil, Recomendações de Aprendizado, Timeline, Métricas de Sucesso
        - Seja específico e forneça exemplos concretos
        - Inclua prazos realistas baseados na disponibilidade do usuário
        - Sugira recursos específicos (cursos, livros, projetos) sempre que possível
        - Considere as preferências de aprendizado do usuário
        - Inclua estimativas salariais quando relevante

        Forneça um plano abrangente e acionável.
        """
        
        return prompt
    
    def _generate_fallback_plan(self, user_profile):
        """Gera um plano de fallback caso a API do Gemini falhe"""
        current_skills = user_profile.get('current_skills', [])
        career_goals = user_profile.get('career_goals', [])
        
        return f"""
        # Plano de Desenvolvimento de Carreira
        
        ## Análise de Perfil
        Com base nas suas habilidades atuais: {', '.join(current_skills)}
        e seus objetivos: {', '.join(career_goals)}
        
        ## Recomendações
        1. Desenvolva habilidades em {career_goals[0] if career_goals else 'sua área de interesse'}
        2. Participe de cursos online na área
        3. Construa projetos práticos para seu portfolio
        
        ## Timeline Estimada
        - 3-6 meses para desenvolvimento das habilidades básicas
        - 6-12 meses para especialização
        
        ## Recursos Recomendados
        - Coursera: Cursos de especialização
        - Udemy: Cursos práticos
        - Livros da área
        - Projetos open source no GitHub
        """