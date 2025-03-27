class TextScramble {
    constructor(el) {
        this.el = el;
        this.chars = "!<>x-_\\/øæå[]{}—=+*^?#____";
        this.update = this.update.bind(this);
    }

    setText(newText) {
        const oldText = this.el.innerText;
        const length = Math.max(oldText.length, newText.length);
        this.queue = this.createQueue(oldText, newText, length);
        cancelAnimationFrame(this.frameRequest);
        this.frame = 0;
        this.update();
        return new Promise((resolve) => (this.resolve = resolve));
    }

    createQueue(oldText, newText, length) {
        const queue = [];
        for (let i = 0; i < length; i++) {
            const from = oldText[i] || "";
            const to = newText[i] || "";
            const start = Math.floor(Math.random() * 40);
            const end = start + Math.floor(Math.random() * 40);
            queue.push({ from, to, start, end });
        }
        return queue;
    }

    update() {
        let output = "";
        let complete = 0;
        for (let i = 0, n = this.queue.length; i < n; i++) {
            let { from, to, start, end, char } = this.queue[i];
            if (this.frame >= end) {
                complete++;
                output += to;
            } else if (this.frame >= start) {
                if (!char || Math.random() < 0.05) {
                    char = this.randomChar();
                    this.queue[i].char = char;
                }
                output += `<span class="dud">${char}</span>`;
            } else {
                output += from;
            }
        }
        this.el.innerHTML = output;
        if (complete === this.queue.length) {
            this.resolve();
        } else {
            this.frameRequest = requestAnimationFrame(this.update);
            this.frame++;
        }
    }

    randomChar() {
        return this.chars[Math.floor(Math.random() * this.chars.length)];
    }
}

const llmSlander = [
    "teaching models to autocomplete my job.",
    "expectation: AGI. reality: AI-generated lorem ipsum.",
    "masked language modeling: hide and seek, but painful.",
    "training expensive parrots with bad memory.",
    "models are too big to fail, too stupid to trust.",
    "scaling laws say 'bigger is better'; real-world constraints say otherwise.",
    "convinced my model to speak 50 languages. none of them well.",
    "optimizing inference speed, not my workflow.",
    "parameter count is a personality trait.",
    "writing tokenizers, questioning my own comprehension.",
    "emergent abilities: unexpected behaviors we take credit for after the fact.",
    "self-attention, but only for models.",
    "trade-offs between generalization, stability, and blowing up your gpu.",
    "cramming the entire internet into a model and then wondering why it hallucinates.",
    "transformers solved NLP, except for all the parts they didn't.",
    "confidently predicting the next word without a clue about the last one.",
    "beam search: choosing the least ridiculous hallucination and calling it 'optimal.'",
    "self-attention: listening to everyone at once but understanding no one.",
    "memorizing word relationships without knowing what a single one actually means.",
    "carefully adjusting a model so it still makes mistakes, just slightly different ones.",
    "'bigger models perform better'—until they hit the real-world limits of compute and energy bills.",
    "attention heads: looking at everything, but still needing prompting to notice the obvious.",
    "tokenization: breaking languages into tiny pieces and trying to glue it back together.",
    "picking the most probable response, even if it’s confidently incorrect.",
    "when in doubt, throw more gpus at the problem.",
    "treating text like a math problem, then being surprised when it lacks common sense.",
    "teaching a model to be just the right amount of wrong.",
    "reading everything but verifying nothing.",
    "adding more layers to focus harder, rather than smarter.",
    "nudging responses until they become a slightly more polished guess."
];

const el = document.querySelector(".text");
const fx = new TextScramble(el);
const next = () => {
    const randomIndex = Math.floor(Math.random() * llmSlander.length);
    fx.setText(llmSlander[randomIndex]).then(() => {
        setTimeout(next, 2000);
    });
};

next();
