// WordRhythm 2D Canvas Battle & Rhythm Arena Renderer (Clean, Modern & Professional UI)
class GameCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.floatingTexts = [];
        this.bossShake = 0;
        this.bossHurtFlash = 0;
        this.bossAttackAnim = 0;
        this.beatPulse = 0;

        // Boss & Player state
        this.bossMaxHp = 100;
        this.bossCurrentHp = 100;
        this.bossDisplayedHp = 100;
        this.bossName = "Boss";
        this.bossTitle = "Guardian";
        this.bossAvatar = "boss_cyber";

        this.playerHp = 3;
        this.playerMaxHp = 3;

        this.initResize();
        this.startLoop();
    }

    initResize() {
        const resize = () => {
            const rect = this.canvas.parentElement.getBoundingClientRect();
            this.canvas.width = Math.min(1000, rect.width || 800);
            this.canvas.height = 360;
        };
        resize();
        window.addEventListener('resize', resize);
    }

    setBoss(name, title, avatar, hp) {
        this.bossName = name;
        this.bossTitle = title;
        this.bossAvatar = avatar || "boss_cyber";
        this.bossMaxHp = hp || 100;
        this.bossCurrentHp = hp || 100;
        this.bossDisplayedHp = hp || 100;
    }

    setPlayerHp(hp) {
        if (hp < this.playerHp) {
            const lostIdx = hp;
            this.spawnHeartShatter(lostIdx);
        }
        this.playerHp = Math.max(0, Math.min(3, hp));
    }

    damageBoss(amount) {
        this.bossCurrentHp = Math.max(0, this.bossCurrentHp - amount);
        this.bossShake = 12;
        this.bossHurtFlash = 10;
        this.spawnFloatingText(`-${amount} HP`, this.canvas.width / 2 + (Math.random() * 30 - 15), 115, "#10b981");
        this.spawnHitBurst(this.canvas.width / 2, 140, "#10b981");
    }

    bossAttack() {
        this.bossAttackAnim = 16;
        this.bossShake = 18;
        this.spawnFloatingText("-1 HP", 120, 45, "#f43f5e");
        this.spawnHitBurst(this.canvas.width / 2, 210, "#f43f5e");
    }

    triggerBeat() {
        this.beatPulse = 1.0;
    }

    spawnFloatingText(text, x, y, color = "#10b981") {
        this.floatingTexts.push({
            text, x, y, color,
            alpha: 1.0,
            vy: -1.2
        });
    }

    spawnHitBurst(x, y, color = "#06b6d4") {
        for (let i = 0; i < 20; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 2 + Math.random() * 4.5;
            this.particles.push({
                x, y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: 1.5 + Math.random() * 2.5,
                color,
                alpha: 1.0,
                decay: 0.03 + Math.random() * 0.02
            });
        }
    }

    spawnHeartShatter(heartIndex) {
        const heartX = 140 + heartIndex * 34;
        const heartY = 32;
        for (let i = 0; i < 16; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 2 + Math.random() * 4;
            this.particles.push({
                x: heartX,
                y: heartY,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: 2 + Math.random() * 2.5,
                color: "#f43f5e",
                alpha: 1.0,
                decay: 0.025
            });
        }
    }

    startLoop() {
        const loop = () => {
            this.update();
            this.render();
            requestAnimationFrame(loop);
        };
        requestAnimationFrame(loop);
    }

    update() {
        this.bossDisplayedHp += (this.bossCurrentHp - this.bossDisplayedHp) * 0.14;

        if (this.bossShake > 0) this.bossShake *= 0.85;
        if (this.bossHurtFlash > 0) this.bossHurtFlash--;
        if (this.bossAttackAnim > 0) this.bossAttackAnim--;
        if (this.beatPulse > 0) this.beatPulse *= 0.90;

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.alpha -= p.decay;
            if (p.alpha <= 0) {
                this.particles.splice(i, 1);
            }
        }

        for (let i = this.floatingTexts.length - 1; i >= 0; i--) {
            const ft = this.floatingTexts[i];
            ft.y += ft.vy;
            ft.alpha -= 0.025;
            if (ft.alpha <= 0) {
                this.floatingTexts.splice(i, 1);
            }
        }
    }

    render() {
        const { ctx, canvas } = this;
        const w = canvas.width;
        const h = canvas.height;

        // 1. Sleek Obsidian Background
        const grad = ctx.createLinearGradient(0, 0, 0, h);
        grad.addColorStop(0, "#080c16");
        grad.addColorStop(0.7, "#0d1322");
        grad.addColorStop(1, "#111827");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // 2. Subtle Grid
        ctx.save();
        ctx.strokeStyle = `rgba(255, 255, 255, ${0.02 + this.beatPulse * 0.03})`;
        ctx.lineWidth = 1;
        const gridSpacing = 44;
        for (let x = 0; x < w; x += gridSpacing) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, h);
            ctx.stroke();
        }
        for (let y = 0; y < h; y += gridSpacing) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(w, y);
            ctx.stroke();
        }
        ctx.restore();

        // 3. Central Subtle Beat Wave Ring
        ctx.save();
        const centerX = w / 2;
        const centerY = 145;
        const ringRadius = 58 + this.beatPulse * 22;
        ctx.strokeStyle = `rgba(16, 185, 129, ${0.15 + this.beatPulse * 0.35})`;
        ctx.lineWidth = 1.5 + this.beatPulse * 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, ringRadius, 0, Math.PI * 2);
        ctx.stroke();
        ctx.restore();

        // 4. Render Boss
        this.renderBoss(centerX, centerY);

        // 5. Render Boss HP Bar & Title
        this.renderBossHUD(w);

        // 6. Render Player Hearts
        this.renderPlayerHUD();

        // 7. Particles
        ctx.save();
        for (const p of this.particles) {
            ctx.globalAlpha = Math.max(0, p.alpha);
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.restore();

        // 8. Floating Texts
        ctx.save();
        ctx.textAlign = "center";
        ctx.font = "bold 17px 'Plus Jakarta Sans', sans-serif";
        for (const ft of this.floatingTexts) {
            ctx.globalAlpha = Math.max(0, ft.alpha);
            ctx.fillStyle = ft.color;
            ctx.fillText(ft.text, ft.x, ft.y);
        }
        ctx.restore();
    }

    renderBoss(cx, cy) {
        const { ctx } = this;
        ctx.save();

        const shakeX = (Math.random() - 0.5) * this.bossShake;
        const shakeY = (Math.random() - 0.5) * this.bossShake;
        const bobY = Math.sin(Date.now() / 280) * 6 * (1 + this.beatPulse * 0.4);

        const bx = cx + shakeX;
        const by = cy + shakeY + bobY;

        // Subtle ground shadow
        ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
        ctx.beginPath();
        ctx.ellipse(bx, cy + 80, 65, 14, 0, 0, Math.PI * 2);
        ctx.fill();

        if (this.bossAvatar === "boss_chef") {
            this.drawChefBoss(ctx, bx, by);
        } else if (this.bossAvatar === "boss_chimera") {
            this.drawChimeraBoss(ctx, bx, by);
        } else if (this.bossAvatar === "boss_monopoly") {
            this.drawMonopolyBoss(ctx, bx, by);
        } else if (this.bossAvatar === "boss_examiner") {
            this.drawExaminerBoss(ctx, bx, by);
        } else if (this.bossAvatar === "boss_shadow") {
            this.drawShadowBoss(ctx, bx, by);
        } else {
            this.drawCyberCoreBoss(ctx, bx, by);
        }

        ctx.restore();
    }

    drawCyberCoreBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#0284c7";
        ctx.beginPath();
        ctx.arc(bx, by, 44, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "#06b6d4";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(bx, by, 54, Date.now() / 450, Date.now() / 450 + Math.PI * 1.5);
        ctx.stroke();

        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 4, 6, 0, Math.PI * 2);
        ctx.arc(bx + 14, by - 4, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#0f172a";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 4, 3, 0, Math.PI * 2);
        ctx.arc(bx + 14, by - 4, 3, 0, Math.PI * 2);
        ctx.fill();
    }

    drawChefBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#e11d48";
        ctx.beginPath();
        ctx.arc(bx, by, 44, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#ffffff";
        ctx.fillRect(bx - 28, by - 65, 56, 22);
        ctx.beginPath();
        ctx.arc(bx - 16, by - 65, 18, 0, Math.PI * 2);
        ctx.arc(bx + 16, by - 65, 18, 0, Math.PI * 2);
        ctx.arc(bx, by - 72, 22, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#0f172a";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 6, 6, 0, Math.PI * 2);
        ctx.arc(bx + 14, by - 6, 6, 0, Math.PI * 2);
        ctx.fill();
    }

    drawChimeraBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#059669";
        ctx.beginPath();
        ctx.arc(bx, by, 44, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#d97706";
        ctx.beginPath();
        ctx.moveTo(bx - 32, by - 24);
        ctx.lineTo(bx - 55, by - 60);
        ctx.lineTo(bx - 18, by - 42);
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(bx + 32, by - 24);
        ctx.lineTo(bx + 55, by - 60);
        ctx.lineTo(bx + 18, by - 42);
        ctx.fill();

        ctx.fillStyle = "#a7f3d0";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 4, 7, 0, Math.PI * 2);
        ctx.arc(bx + 14, by - 4, 7, 0, Math.PI * 2);
        ctx.fill();
    }

    drawMonopolyBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#7c3aed";
        ctx.beginPath();
        ctx.arc(bx, by, 44, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#f59e0b";
        ctx.fillRect(bx - 36, by - 44, 72, 7);
        ctx.fillRect(bx - 24, by - 78, 48, 36);

        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 4, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "#f59e0b";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.arc(bx + 14, by - 4, 9, 0, Math.PI * 2);
        ctx.stroke();
    }

    drawExaminerBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#3730a3";
        ctx.beginPath();
        ctx.arc(bx, by, 46, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#4f46e5";
        ctx.beginPath();
        ctx.moveTo(bx, by - 72);
        ctx.lineTo(bx + 50, by - 48);
        ctx.lineTo(bx, by - 34);
        ctx.lineTo(bx - 50, by - 48);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = "#38bdf8";
        ctx.fillRect(bx - 26, by - 8, 52, 8);
    }

    drawShadowBoss(ctx, bx, by) {
        ctx.fillStyle = this.bossHurtFlash > 0 ? "#f43f5e" : "#1f2937";
        ctx.beginPath();
        ctx.arc(bx, by, 46, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "#f43f5e";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(bx, by, 54 + Math.sin(Date.now() / 200) * 4, 0, Math.PI * 2);
        ctx.stroke();

        ctx.fillStyle = "#f43f5e";
        ctx.beginPath();
        ctx.arc(bx - 14, by - 4, 5, 0, Math.PI * 2);
        ctx.arc(bx + 14, by - 4, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    renderBossHUD(w) {
        const { ctx } = this;
        const barWidth = Math.min(380, w * 0.52);
        const barX = (w - barWidth) / 2;
        const barY = 22;

        ctx.save();
        ctx.textAlign = "center";
        ctx.font = "bold 13.5px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = "#f8fafc";
        ctx.fillText(`${this.bossTitle.toUpperCase()} • ${this.bossName}`, w / 2, barY - 6);

        // HP Bar background
        ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
        ctx.fillRect(barX, barY, barWidth, 14);

        // HP Fill
        const hpPercent = Math.max(0, this.bossDisplayedHp / this.bossMaxHp);
        const fillW = Math.max(0, barWidth * hpPercent);

        if (fillW > 0) {
            ctx.fillStyle = hpPercent > 0.4 ? "#10b981" : (hpPercent > 0.2 ? "#f59e0b" : "#f43f5e");
            ctx.fillRect(barX, barY, fillW, 14);
        }

        ctx.font = "bold 10px 'JetBrains Mono', monospace";
        ctx.fillStyle = "#ffffff";
        ctx.fillText(`${Math.round(this.bossCurrentHp)} / ${this.bossMaxHp} HP`, w / 2, barY + 11);
        ctx.restore();
    }

    renderPlayerHUD() {
        const { ctx } = this;
        ctx.save();

        ctx.font = "600 11px 'Plus Jakarta Sans', sans-serif";
        ctx.fillStyle = "#94a3b8";
        ctx.fillText("PLAYER HP", 24, 30);

        for (let i = 0; i < 3; i++) {
            const hx = 105 + i * 28;
            const hy = 22;
            const isAlive = i < this.playerHp;

            ctx.save();
            ctx.fillStyle = isAlive ? "#f43f5e" : "rgba(255, 255, 255, 0.12)";
            this.drawHeart(ctx, hx, hy, 12);
            ctx.restore();
        }

        ctx.restore();
    }

    drawHeart(ctx, x, y, size) {
        ctx.beginPath();
        const topCurveHeight = size * 0.3;
        ctx.moveTo(x, y + topCurveHeight);
        ctx.bezierCurveTo(x, y, x - size / 2, y, x - size / 2, y + topCurveHeight);
        ctx.bezierCurveTo(x - size / 2, y + (size + topCurveHeight) / 2, x, y + (size + topCurveHeight) / 1.5, x, y + size);
        ctx.bezierCurveTo(x, y + (size + topCurveHeight) / 1.5, x + size / 2, y + (size + topCurveHeight) / 2, x + size / 2, y + topCurveHeight);
        ctx.bezierCurveTo(x + size / 2, y, x, y, x, y + topCurveHeight);
        ctx.closePath();
        ctx.fill();
    }
}

window.GameCanvas = GameCanvas;
