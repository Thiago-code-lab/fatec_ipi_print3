// Estado da aplicação
let currentUser = null;
let authToken = localStorage.getItem('authToken');
let currentItinerary = null;

// Elementos da interface
const loginScreen = document.getElementById('login-screen');
const loginForm = document.getElementById('login-form');
const appContent = document.getElementById('app-content');
const itineraryList = document.getElementById('itinerary-list');
const dayDetails = document.getElementById('day-details');
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const chatContainer = document.getElementById('chat-container');

// Configuração da API
const API_BASE_URL = 'http://localhost:5000/api';

// Funções de autenticação
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            currentUser = data.user;
            localStorage.setItem('authToken', authToken);
            showApp();
            loadItinerary();
        } else {
            showError('Erro ao fazer login: ' + (data.message || 'Credenciais inválidas'));
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error);
        showError('Erro ao conectar ao servidor. Por favor, tente novamente.');
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showLogin();
}

// Funções para gerenciar a interface
function showLogin() {
    loginScreen.style.display = 'flex';
    appContent.style.display = 'none';
    document.title = 'Login - Tour4Friends';
}

function showApp() {
    loginScreen.style.display = 'none';
    appContent.style.display = 'block';
    document.title = 'Tour4Friends - Caminho de Santiago';
}

function showError(message) {
    alert(message); // Em uma aplicação real, você pode querer mostrar isso de forma mais elegante
}

// Funções para carregar dados
async function loadItinerary() {
    try {
        const response = await fetch(`${API_BASE_URL}/itinerary`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.status === 401) {
            logout();
            return;
        }
        
        if (!response.ok) {
            throw new Error('Erro ao carregar o roteiro');
        }
        
        currentItinerary = await response.json();
        renderItinerary(currentItinerary);
    } catch (error) {
        console.error('Erro ao carregar roteiro:', error);
        showError('Não foi possível carregar o roteiro. Tente novamente mais tarde.');
    }
}

async function loadDayMap(dayId) {
    try {
        const response = await fetch(`${API_BASE_URL}/days/${dayId}/map`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            renderDayMap(dayId, data);
        }
    } catch (error) {
        console.error('Erro ao carregar mapa do dia:', error);
    }
}

// Funções de renderização
function renderItinerary(itinerary) {
    document.getElementById('itinerary-title').textContent = itinerary.title;
    
    const daysList = itinerary.days.map(day => `
        <div class="day-card" onclick="selectDay(${day.id})">
            <h3>Dia ${day.day_number}: ${day.start_location} → ${day.end_location}</h3>
            <div class="day-info">
                <span><i class="fas fa-route"></i> ${day.distance_km} km</span>
                <span><i class="far fa-calendar-alt"></i> ${formatDate(day.date)}</span>
            </div>
            ${day.notes ? `<p class="day-notes">${day.notes}</p>` : ''}
            ${day.pois && day.pois.length > 0 ? 
                `<div class="poi-count"><i class="fas fa-map-marker-alt"></i> ${day.pois.length} pontos de interesse</div>` : ''}
        </div>
    `).join('');
    
    itineraryList.innerHTML = daysList || '<p>Nenhum dia de roteiro disponível.</p>';
}

function renderDayMap(dayId, dayData) {
    const day = currentItinerary.days.find(d => d.id === dayId);
    if (!day) return;
    
    // Esconde a lista de dias e mostra os detalhes do dia
    document.getElementById('itinerary-list').style.display = 'none';
    
    // Cria o conteúdo dos detalhes do dia
    dayDetails.style.display = 'block';
    dayDetails.innerHTML = `
        <button class="back-button" onclick="backToList()">
            <i class="fas fa-arrow-left"></i> Voltar para a lista
        </button>
        <h3>Dia ${day.day_number}: ${day.start_location} → ${day.end_location}</h3>
        <div class="day-info">
            <span><i class="fas fa-calendar-day"></i> ${formatDate(day.date)}</span>
            <span><i class="fas fa-route"></i> ${day.distance_km} km</span>
        </div>
        
        ${day.notes ? `<div class="day-notes"><p>${day.notes}</p></div>` : ''}
        
        <div class="map-container" id="map-container">
            <p>Carregando mapa...</p>
            <!-- O mapa será renderizado aqui pelo Google Maps API -->
        </div>
        
        <div class="pois-list">
            <h4><i class="fas fa-map-marker-alt"></i> Pontos de Interesse</h4>
            ${day.pois && day.pois.length > 0 
                ? day.pois.map(poi => `
                    <div class="poi">
                        <strong>${poi.name}</strong>
                        <p>${poi.description}</p>
                    </div>
                `).join('')
                : '<p>Nenhum ponto de interesse cadastrado para este dia.</p>'
            }
        </div>
        
        <div class="lodging-info">
            <h4><i class="fas fa-hotel"></i> Hospedagem</h4>
            <p>${day.lodging_info || 'Nenhuma informação de hospedagem disponível.'}</p>
        </div>
    `;
    
    // Inicializa o mapa (simulação, pois precisaria da API do Google Maps)
    initializeMap(dayData);
}

function initializeMap(dayData) {
    // Esta é uma simulação. Em uma implementação real, você usaria a API do Google Maps
    const mapContainer = document.getElementById('map-container');
    
    // Simulação de um mapa
    setTimeout(() => {
        mapContainer.innerHTML = `
            <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #e9f5f4; border-radius: 8px; color: #0d9488;">
                <div style="text-align: center; padding: 20px;">
                    <i class="fas fa-map-marked-alt" style="font-size: 3rem; margin-bottom: 10px;"></i>
                    <h3>Mapa do Trajeto</h3>
                    <p>${dayData.day.start_location} → ${dayData.day.end_location}</p>
                    <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">
                        Em uma implementação real, aqui estaria um mapa interativo mostrando o trajeto.
                    </p>
                </div>
            </div>
        `;
    }, 500);
}

function backToList() {
    dayDetails.style.display = 'none';
    dayDetails.innerHTML = '';
    document.getElementById('itinerary-list').style.display = 'block';
}

function selectDay(dayId) {
    loadDayMap(dayId);
}

// Funções para o chat
function toggleChat() {
    chatContainer.classList.toggle('visible');
}

function addMessage(text, sender = 'user') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender} fade-in`;
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-time">${timeString}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Funções auxiliares
function formatDate(dateString) {
    if (!dateString) return '';
    
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        timeZone: 'UTC' // Para evitar problemas com timezone
    };
    
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Verifica se o usuário já está autenticado
    if (authToken) {
        showApp();
        loadItinerary();
    } else {
        showLogin();
    }
    
    // Configura o formulário de login
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            login(email, password);
        });
    }
    
    // Configura o formulário do chat
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = chatForm.querySelector('input');
            const message = input.value.trim();
            
            if (message) {
                // Adiciona a mensagem do usuário
                addMessage(message, 'user');
                
                // Simula uma resposta automática após um pequeno atraso
                setTimeout(() => {
                    addMessage("Obrigado pela sua mensagem! Nossa equipe de suporte entrará em contato em breve.", 'support');
                }, 1000);
                
                // Limpa o campo de entrada
                input.value = '';
            }
        });
    }
});

// Funções globais para serem acessíveis via HTML
window.toggleChat = toggleChat;
window.selectDay = selectDay;
window.backToList = backToList;
window.logout = logout;
