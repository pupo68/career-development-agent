import json
import os
from datetime import datetime

class CareerDevelopmentAgent:
    def __init__(self):
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
                print(f"Arquivo {filename} não encontrado em {knowledge_dir}")
                knowledge[key] = {}
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON do arquivo {filename}")
                knowledge[key] = {}
        
        return knowledge
    
    def analyze_profile(self, user_profile):
        """Analisa o perfil do usuário e gera um plano de desenvolvimento de carreira"""
        # Extrai informações do perfil do usuário
        current_skills = user_profile.get('current_skills', [])
        career_goals = user_profile.get('career_goals', [])
        industry = user_profile.get('industry', '')
        years_experience = user_profile.get('years_experience', 0)
        learning_preferences = user_profile.get('learning_preferences', [])
        time_commitment = user_profile.get('time_commitment', '')
        
        # Inicia a construção da resposta
        response = "# Plano de Desenvolvimento de Carreira\n\n"
        
        # Adiciona uma análise personalizada
        response += self._generate_analysis(current_skills, career_goals, industry, years_experience)
        
        # Adiciona recomendações de aprendizado
        response += self._generate_learning_recommendations(career_goals, learning_preferences, time_commitment)
        
        # Adiciona informações sobre salários e certificações, se disponíveis
        response += self._generate_additional_info(career_goals, industry)
        
        return response
    
    def _generate_analysis(self, current_skills, career_goals, industry, years_experience):
        """Gera a análise de perfil"""
        section = "## Análise de Perfil\n\n"
        
        # Análise de habilidades atuais
        section += f"- **Habilidades atuais**: {', '.join(current_skills) if current_skills else 'Nenhuma informada'}\n"
        section += f"- **Objetivos de carreira**: {', '.join(career_goals) if career_goals else 'Nenhum informado'}\n"
        section += f"- **Setor/Indústria**: {industry}\n"
        section += f"- **Anos de experiência**: {years_experience}\n\n"
        
        # Identifica gaps de habilidades com base nas tendências
        in_demand_skills = self.knowledge.get('trends', {}).get('in_demand_skills_2025', [])
        missing_skills = [skill for skill in in_demand_skills if skill not in current_skills]
        
        if missing_skills:
            section += "### Habilidades em Alta Demandadas\n"
            section += "Com base nas tendências atuais, as seguintes habilidades estão em alta e podem ser úteis para seus objetivos:\n"
            for skill in missing_skills[:5]:  # Limita a 5 habilidades para não ficar muito longo
                section += f"- {skill}\n"
            section += "\n"
        
        return section
    
    def _generate_learning_recommendations(self, career_goals, learning_preferences, time_commitment):
        """Gera recomendações de aprendizado personalizadas"""
        section = "## Recomendações de Aprendizado\n\n"
        
        # Se não houver objetivos de carreira, retorna uma mensagem genérica
        if not career_goals:
            section += "Para começar, defina alguns objetivos de carreira para receber recomendações personalizadas.\n\n"
            return section
        
        # Para cada objetivo de carreira, busca recomendações
        for goal in career_goals:
            # Tenta encontrar um caminho de aprendizado correspondente
            learning_path = self.knowledge.get('learning_paths', {}).get(goal, {})
            if learning_path:
                section += f"### Para se tornar {goal}\n"
                
                # Recursos recomendados
                resources = learning_path.get('resources', {})
                if resources:
                    section += "#### Recursos Recomendados:\n"
                    if resources.get('courses'):
                        section += "- **Cursos**:\n"
                        for course in resources['courses'][:3]:
                            section += f"  - {course}\n"
                    if resources.get('books'):
                        section += "- **Livros**:\n"
                        for book in resources['books'][:3]:
                            section += f"  - {book}\n"
                    if resources.get('projects'):
                        section += "- **Projetos**:\n"
                        for project in resources['projects'][:3]:
                            section += f"  - {project}\n"
                
                # Timeline baseada na disponibilidade de tempo
                timeline = learning_path.get('timeline', {})
                if timeline and time_commitment:
                    section += f"#### Timeline Estimada ({time_commitment} por semana):\n"
                    for stage, duration in timeline.items():
                        section += f"- **{stage}**: {duration}\n"
                
                section += "\n"
            else:
                section += f"### {goal}\n"
                section += f"Não encontramos um caminho de aprendizado específico para {goal}. Recomendamos buscar cursos e recursos genéricos na área.\n\n"
        
        return section
    
    def _generate_additional_info(self, career_goals, industry):
        """Gera informações adicionais sobre salários e certificações"""
        section = "## Informações Adicionais\n\n"
        
        # Informações salariais
        salary_data = self.knowledge.get('salary_data', {})
        if salary_data:
            section += "### Faixas Salariais (por ano, em USD)\n"
            # Mostra salários para os objetivos de carreira, se disponíveis
            for goal in career_goals:
                # Tenta encontrar dados salariais para o objetivo
                found = False
                for region, jobs in salary_data.items():
                    if goal in jobs:
                        section += f"- **{goal}** em {region}: Entry: ${jobs[goal]['entry_level']:,} | Senior: ${jobs[goal]['senior_level']:,}\n"
                        found = True
                        break
                if not found:
                    section += f"- **{goal}**: Dados salariais não disponíveis.\n"
            section += "\n"
        
        # Certificações
        certifications = self.knowledge.get('certifications', {})
        if certifications:
            section += "### Certificações Recomendadas\n"
            for goal in career_goals:
                if goal in certifications:
                    section += f"- **{goal}**:\n"
                    for cert in certifications[goal][:2]:  # Limita a 2 certificações por objetivo
                        section += f"  - {cert['name']} ({cert['provider']}) - Custo: {cert['cost']}\n"
            section += "\n"
        
        return section