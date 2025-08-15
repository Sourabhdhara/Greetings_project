class AnimatedTimeGreeting {
    constructor() {
        this.canvas = document.getElementById('backgroundCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.animationFrame = 0;
        this.starPositions = [];
        
        this.initCanvas();
        this.initStars();
        this.updateDisplay();
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    initCanvas() {
        this.handleResize();
    }
    
    handleResize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    initStars() {
        this.starPositions = [];
        for (let i = 0; i < 50; i++) {
            this.starPositions.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * (window.innerHeight * 0.4),
                size: Math.random() * 2 + 1,
                speed: Math.random() * 0.02 + 0.01
            });
        }
    }
    
    getTimeData() {
        const now = new Date();
        const h = now.getHours();
        const m = now.getMinutes();
        const s = now.getSeconds();
        
        const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const months = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];
        
        const day = days[now.getDay()];
        const date = `${now.getDate()} ${months[now.getMonth()]}, ${now.getFullYear()}`;
        const time = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        let greeting, period;
        
        if (h >= 0 && h < 12) {
            greeting = "Good Morning";
            period = "morning";
        } else if (h >= 12 && h < 17) {
            greeting = "Good Afternoon";
            period = "afternoon";
        } else if (h >= 17 && h < 20) {
            greeting = "Good Evening";
            period = "evening";
        } else {
            greeting = "Good Night";
            period = "night";
        }
        
        return { greeting, day, date, time, period, h, m, s };
    }
    
    getThemeColors(period) {
        const themes = {
            morning: {
                bgGradient: ['#87CEEB', '#FFE4B5', '#FFA07A'],
                accent: '#FFD700',
                secondary: '#FF6347'
            },
            afternoon: {
                bgGradient: ['#F0E68C', '#FFD700', '#FFA500'],
                accent: '#FF8C00',
                secondary: '#DAA520'
            },
            evening: {
                bgGradient: ['#9370DB', '#8A2BE2', '#4B0082'],
                accent: '#FF1493',
                secondary: '#FF69B4'
            },
            night: {
                bgGradient: ['#191970', '#000080', '#0F0F23'],
                accent: '#4169E1',
                secondary: '#6495ED'
            }
        };
        return themes[period];
    }
    
    drawGradientBackground(colors) {
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
        gradient.addColorStop(0, colors[0]);
        gradient.addColorStop(0.5, colors[1]);
        gradient.addColorStop(1, colors[2]);
        
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
    
    drawMorningAnimation(theme) {
        this.drawGradientBackground(theme.bgGradient);
        
        // Animated sun
        const sunX = this.canvas.width * 0.2;
        const sunY = this.canvas.height * 0.2;
        const sunSize = 60 + 15 * Math.sin(this.animationFrame * 0.02);
        
        // Sun glow
        const glowGradient = this.ctx.createRadialGradient(sunX, sunY, 0, sunX, sunY, sunSize + 30);
        glowGradient.addColorStop(0, 'rgba(255, 215, 0, 0.8)');
        glowGradient.addColorStop(1, 'rgba(255, 215, 0, 0)');
        this.ctx.fillStyle = glowGradient;
        this.ctx.fillRect(sunX - sunSize - 30, sunY - sunSize - 30, (sunSize + 30) * 2, (sunSize + 30) * 2);
        
        // Sun body
        this.ctx.beginPath();
        this.ctx.arc(sunX, sunY, sunSize, 0, Math.PI * 2);
        this.ctx.fillStyle = '#FFD700';
        this.ctx.fill();
        this.ctx.strokeStyle = '#FFA500';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
        
        // Sun rays
        this.ctx.strokeStyle = '#FFD700';
        this.ctx.lineWidth = 4;
        for (let i = 0; i < 8; i++) {
            const angle = (i * 45 + this.animationFrame) * Math.PI / 180;
            const startX = sunX + (sunSize + 15) * Math.cos(angle);
            const startY = sunY + (sunSize + 15) * Math.sin(angle);
            const endX = sunX + (sunSize + 40) * Math.cos(angle);
            const endY = sunY + (sunSize + 40) * Math.sin(angle);
            
            this.ctx.beginPath();
            this.ctx.moveTo(startX, startY);
            this.ctx.lineTo(endX, endY);
            this.ctx.stroke();
        }
    }
    
    drawAfternoonAnimation(theme) {
        this.drawGradientBackground(theme.bgGradient);
        
        // Bright sun
        const sunX = this.canvas.width * 0.8;
        const sunY = this.canvas.height * 0.15;
        
        for (let i = 0; i < 3; i++) {
            const size = 50 - i * 8 + 8 * Math.sin(this.animationFrame * 0.02 + i);
            const alpha = 1.0 - i * 0.25;
            
            this.ctx.beginPath();
            this.ctx.arc(sunX, sunY, size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 215, 0, ${alpha})`;
            this.ctx.fill();
        }
        
        // Moving clouds
        for (let i = 0; i < 3; i++) {
            const cloudX = (this.canvas.width * 0.3 * i + this.animationFrame * 0.5) % (this.canvas.width + 100);
            const cloudY = this.canvas.height * 0.25 + i * 30;
            this.drawCloud(cloudX, cloudY, 40 + i * 10, 'rgba(255, 255, 255, 0.7)');
        }
    }
    
    drawEveningAnimation(theme) {
        this.drawGradientBackground(theme.bgGradient);
        
        // Setting sun
        const sunX = this.canvas.width * 0.15 + 30 * Math.sin(this.animationFrame * 0.01);
        const sunY = this.canvas.height * 0.7;
        
        this.ctx.beginPath();
        this.ctx.arc(sunX, sunY, 40, 0, Math.PI * 2);
        this.ctx.fillStyle = '#FF4500';
        this.ctx.fill();
        this.ctx.strokeStyle = '#FF1493';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
        
        // Floating particles
        for (let i = 0; i < 15; i++) {
            const x = (100 + i * 80 + this.animationFrame * 0.3) % (this.canvas.width + 50);
            const y = this.canvas.height * 0.4 + 80 * Math.sin((x + i * 150) * 0.005);
            const size = 4 + 3 * Math.sin(this.animationFrame * 0.02 + i);
            
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fillStyle = '#FF69B4';
            this.ctx.fill();
        }
    }
    
    drawNightAnimation(theme) {
        this.drawGradientBackground(theme.bgGradient);
        
        // Twinkling stars
        this.starPositions.forEach((star, index) => {
            const brightness = 0.5 + 0.5 * Math.sin(this.animationFrame * star.speed + index);
            const size = star.size * (0.5 + brightness);
            const alpha = brightness;
            
            this.ctx.beginPath();
            this.ctx.arc(star.x, star.y, size, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            this.ctx.fill();
            
            // Star twinkle effect
            if (brightness > 0.8) {
                this.ctx.beginPath();
                this.ctx.arc(star.x, star.y, size + 2, 0, Math.PI * 2);
                this.ctx.fillStyle = `rgba(173, 216, 230, ${brightness - 0.8})`;
                this.ctx.fill();
            }
        });
        
        // Moon with glow
        const moonX = this.canvas.width * 0.8;
        const moonY = this.canvas.height * 0.2;
        const moonGlow = 8 * Math.sin(this.animationFrame * 0.01);
        
        // Moon glow
        const moonGlowGradient = this.ctx.createRadialGradient(moonX, moonY, 0, moonX, moonY, 50 + moonGlow);
        moonGlowGradient.addColorStop(0, 'rgba(230, 230, 250, 0.3)');
        moonGlowGradient.addColorStop(1, 'rgba(230, 230, 250, 0)');
        this.ctx.fillStyle = moonGlowGradient;
        this.ctx.fillRect(moonX - 60, moonY - 60, 120, 120);
        
        // Moon body
        this.ctx.beginPath();
        this.ctx.arc(moonX, moonY, 35, 0, Math.PI * 2);
        this.ctx.fillStyle = '#E6E6FA';
        this.ctx.fill();
        this.ctx.strokeStyle = '#D3D3D3';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
    }
    
    drawCloud(x, y, size, color) {
        this.ctx.fillStyle = color;
        
        // Cloud parts
        this.ctx.beginPath();
        this.ctx.arc(x, y, size * 0.5, 0, Math.PI * 2);
        this.ctx.arc(x + size * 0.7, y, size * 0.6, 0, Math.PI * 2);
        this.ctx.arc(x + size * 1.3, y, size * 0.5, 0, Math.PI * 2);
        this.ctx.arc(x + size * 0.35, y - size * 0.4, size * 0.4, 0, Math.PI * 2);
        this.ctx.arc(x + size * 0.85, y - size * 0.3, size * 0.45, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    updateDisplay() {
        const { greeting, day, date, time, period } = this.getTimeData();
        const theme = this.getThemeColors(period);
        
        // Update DOM elements
        document.getElementById('greeting').textContent = greeting;
        document.getElementById('day').textContent = day;
        document.getElementById('date').textContent = date;
        document.getElementById('time').textContent = time;
        
        // Update theme class
        document.body.className = period;
        
        // Clear and draw background
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw appropriate animation
        switch (period) {
            case 'morning':
                this.drawMorningAnimation(theme);
                break;
            case 'afternoon':
                this.drawAfternoonAnimation(theme);
                break;
            case 'evening':
                this.drawEveningAnimation(theme);
                break;
            case 'night':
                this.drawNightAnimation(theme);
                break;
        }
        
        // Update animation frame
        this.animationFrame += 1;
        if (this.animationFrame > 360) {
            this.animationFrame = 0;
        }
        
        // Schedule next update
        requestAnimationFrame(() => this.updateDisplay());
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AnimatedTimeGreeting();
});
