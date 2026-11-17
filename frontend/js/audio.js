// WordRhythm Audio Engine (Web Audio API Synthesizer & Speech Engine)
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.isMuted = false;
        this.bgmVolume = 0.45;
        this.sfxVolume = 0.7;
        this.voiceEnabled = true;

        // Metronome synth loop
        this.bpm = 120;
        this.isPlayingBgm = false;
        this.nextNoteTime = 0;
        this.beatCount = 0;
        this.timerId = null;

        // Speech synthesis voice
        this.englishVoice = null;
        this.initSpeech();
    }

    initAudioContext() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    initSpeech() {
        if ('speechSynthesis' in window) {
            const loadVoices = () => {
                const voices = window.speechSynthesis.getVoices();
                // Prefer British or American English voice
                this.englishVoice = voices.find(v => v.lang === 'en-GB' || v.name.includes('UK') || v.name.includes('British')) ||
                                   voices.find(v => v.lang === 'en-US' || v.name.includes('US') || v.name.includes('American')) ||
                                   voices.find(v => v.lang.startsWith('en')) || null;
            };
            loadVoices();
            if (window.speechSynthesis.onvoiceschanged !== undefined) {
                window.speechSynthesis.onvoiceschanged = loadVoices;
            }
        }
    }

    speakWord(word, onEndCallback = null) {
        if (!this.voiceEnabled || !('speechSynthesis' in window)) return;
        try {
            window.speechSynthesis.cancel(); // Stop prior speech
            const utterance = new SpeechSynthesisUtterance(word);
            if (this.englishVoice) {
                utterance.voice = this.englishVoice;
            }
            utterance.rate = 0.88; // clear natural pronunciation speed
            utterance.pitch = 1.0;
            if (onEndCallback) {
                utterance.onend = onEndCallback;
            }
            window.speechSynthesis.speak(utterance);
        } catch (e) {
            console.error("Speech synthesis error:", e);
        }
    }

    // --- Sound Effects using Web Audio API synthesis ---

    playKick(time) {
        if (this.isMuted) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.frequency.setValueAtTime(140, time);
        osc.frequency.exponentialRampToValueAtTime(0.01, time + 0.35);

        gain.gain.setValueAtTime(this.bgmVolume * 0.9, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.35);

        osc.start(time);
        osc.stop(time + 0.35);
    }

    playHiHat(time, open = false) {
        if (this.isMuted) return;
        // Synthesize metallic noise
        const bufferSize = this.ctx.sampleRate * (open ? 0.12 : 0.04);
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const filter = this.ctx.createBiquadFilter();
        filter.type = "highpass";
        filter.frequency.value = 7500;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(this.bgmVolume * (open ? 0.35 : 0.25), time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + (open ? 0.12 : 0.04));

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        noise.start(time);
    }

    playSnare(time) {
        if (this.isMuted) return;
        // Tone
        const osc = this.ctx.createOscillator();
        const oscGain = this.ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(180, time);
        osc.frequency.exponentialRampToValueAtTime(40, time + 0.15);
        oscGain.gain.setValueAtTime(this.bgmVolume * 0.5, time);
        oscGain.gain.exponentialRampToValueAtTime(0.01, time + 0.15);
        osc.connect(oscGain);
        oscGain.connect(this.ctx.destination);
        osc.start(time);
        osc.stop(time + 0.15);

        // Noise
        this.playHiHat(time, true);
    }

    playSynthBass(time, freq = 110) {
        if (this.isMuted) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(freq, time);

        const filter = this.ctx.createBiquadFilter();
        filter.type = "lowpass";
        filter.frequency.setValueAtTime(600, time);
        filter.frequency.exponentialRampToValueAtTime(150, time + 0.25);

        gain.gain.setValueAtTime(this.bgmVolume * 0.4, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.25);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(time);
        osc.stop(time + 0.25);
    }

    // High level gameplay SFX
    playHitPerfect() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => { // C Major Chord Arp
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(freq, time + i * 0.035);
            gain.gain.setValueAtTime(this.sfxVolume * 0.35, time + i * 0.035);
            gain.gain.exponentialRampToValueAtTime(0.001, time + i * 0.035 + 0.28);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(time + i * 0.035);
            osc.stop(time + i * 0.035 + 0.28);
        });
    }

    playHitGreat() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        [587.33, 880].forEach((freq, i) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, time + i * 0.04);
            gain.gain.setValueAtTime(this.sfxVolume * 0.35, time + i * 0.04);
            gain.gain.exponentialRampToValueAtTime(0.001, time + i * 0.04 + 0.22);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(time + i * 0.04);
            osc.stop(time + i * 0.04 + 0.22);
        });
    }

    playMiss() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(140, time);
        osc.frequency.exponentialRampToValueAtTime(50, time + 0.25);
        gain.gain.setValueAtTime(this.sfxVolume * 0.45, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.25);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(time);
        osc.stop(time + 0.25);
    }

    playBossDamage() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "square";
        osc.frequency.setValueAtTime(440, time);
        osc.frequency.exponentialRampToValueAtTime(110, time + 0.3);
        gain.gain.setValueAtTime(this.sfxVolume * 0.5, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(time);
        osc.stop(time + 0.3);
    }

    playPlayerHurt() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(220, time);
        osc.frequency.linearRampToValueAtTime(60, time + 0.35);
        gain.gain.setValueAtTime(this.sfxVolume * 0.6, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.35);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(time);
        osc.stop(time + 0.35);
    }

    playVictory() {
        this.initAudioContext();
        if (this.isMuted) return;
        const time = this.ctx.currentTime;
        const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51];
        notes.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(freq, time + idx * 0.12);
            gain.gain.setValueAtTime(this.sfxVolume * 0.4, time + idx * 0.12);
            gain.gain.exponentialRampToValueAtTime(0.001, time + idx * 0.12 + 0.5);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(time + idx * 0.12);
            osc.stop(time + idx * 0.12 + 0.5);
        });
    }

    // --- Dynamic BPM Rhythm Metronome Background Loop ---
    startRhythmTrack(bpm = 120, onBeatCallback = null) {
        this.initAudioContext();
        this.bpm = bpm;
        this.isPlayingBgm = true;
        this.beatCount = 0;
        const secondsPerBeat = 60.0 / this.bpm;
        this.nextNoteTime = this.ctx.currentTime + 0.05;

        const scheduleBeat = () => {
            while (this.nextNoteTime < this.ctx.currentTime + 0.15) {
                const beat = this.beatCount % 4; // 4/4 time signature
                const time = this.nextNoteTime;

                // Drum pattern
                if (beat === 0) {
                    this.playKick(time);
                    this.playSynthBass(time, 98); // G1
                } else if (beat === 2) {
                    this.playSnare(time);
                    this.playSynthBass(time, 130.8); // C2
                } else {
                    this.playHiHat(time, false);
                    this.playSynthBass(time, 110); // A1
                }

                // Eighth note hihat groove
                this.playHiHat(time + secondsPerBeat / 2, true);

                if (onBeatCallback) {
                    const delayMs = Math.max(0, (time - this.ctx.currentTime) * 1000);
                    setTimeout(() => {
                        if (this.isPlayingBgm) {
                            onBeatCallback(this.beatCount, this.bpm);
                        }
                    }, delayMs);
                }

                this.beatCount++;
                this.nextNoteTime += secondsPerBeat;
            }

            if (this.isPlayingBgm) {
                this.timerId = setTimeout(scheduleBeat, 35);
            }
        };

        scheduleBeat();
    }

    stopRhythmTrack() {
        this.isPlayingBgm = false;
        if (this.timerId) {
            clearTimeout(this.timerId);
            this.timerId = null;
        }
    }
}

window.soundEngine = new SoundEngine();
