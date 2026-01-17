class OverlayContainer extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.animations = {
      enter: [
        { opacity: 0, transform: 'translateY(-50px)' },
        { opacity: 1, transform: 'translateY(0)' }
      ],
      exit: [
        { opacity: 1 },
        { opacity: 0 }
      ]
    };
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: flex;
          justify-content: center;
          margin-top: 5rem;
        }

        * {
          box-sizing: border-box;
          margin: 0;
        }

        :host {
          --branding-green: hsl(107, 38%, 50%);
          --branding-blue: hsl(209, 30%, 50%);

          --branding-bg-blue: hsl(209, 30%, 10%);
          --branding-bg-green: hsl(107, 38%, 45%);
          --bg-light-grey: hsla(0, 10%, 95%, 0.7);
          --bg-light-grey--darker: hsla(0, 10%, 90%, 0.7);

          --header-font-size: 1.25rem;
          --header-height: calc(var(--header-font-size) * 2.25);

          font-family: Ethnocentric, sans-serif;
        }

        .outline * {
          outline: 1px solid orange;
        }

        #container {
          height: fit-content;
          min-width: 50%;
        }

        #container header {
          position: relative;
          padding: 1rem 2rem;

          z-index: 200;

          min-height: 5rem;
        }

        header > span {
          position: relative;
          z-index: 100;
        }

        header .bg-rect {
          position: absolute;

          border-radius: 4px;

          inset: 0;

          width: 100%;
          height: 100%;
        }

        header #grn-bg {
          background: var(--branding-green);
          transform: skew(19deg);
          width: calc(100% + 0.75rem);
        }

        header #blu-bg {
          background: #0E141A;
          background: linear-gradient(0deg,rgba(14, 20, 26, 1) 0%, rgba(38, 55, 71, 1) 51%);
          transform: skew(19deg) translate(6px, 4px);
        }

        header img {
          height: 22px;
          z-index: 1000;
          position: absolute;
          transform: scale(7) translate(0.65rem, 0.145rem);
        }

        main {
          width: 1000px;
          padding: 1.5rem 2rem;

          position: relative;
          transform: translate(1rem, -0.5rem);

          background: linear-gradient(90deg, var(--bg-light-grey) 65%, var(--bg-light-grey--darker) 100%);
        }

        main .text {
          font-size: 1.125rem;
          grid-area: text;

          min-height: 40vh;
        }

        @keyframes slideIn {
          0% {
            opacity: 0;
            transform: translateY(-50px);
          }

          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeOut {
          0% {
            opacity: 1;
          }

          100% {
            opacity: 0;
          }
        }
      </style>

      <div id="container">
        <header>
          <div id="grn-bg" class="bg-rect"></div>
          <div id="blu-bg" class="bg-rect"></div>

          <img src="./TDK Motorsports 2-02_transparent.png" alt="" style="height: 24px;">
        </header>
        <main>
          <slot></slot>
        </main>
      </div>
    `;
  }

  // Method to get the main element for content manipulation
  get mainElement() {
    return this.shadowRoot.querySelector('main');
  }

  // Method to animate content in
  animateIn(element, options = {}) {
    const duration = options.duration || 500;
    const easing = options.easing || 'ease-out';

    return element.animate(this.animations.enter, {
      duration,
      easing,
      fill: 'forwards'
    });
  }

  // Method to animate content out
  animateOut(element, options = {}) {
    const duration = options.duration || 300;
    const easing = options.easing || 'ease-in';

    return element.animate(this.animations.exit, {
      duration,
      easing,
      fill: 'forwards'
    });
  }
}

customElements.define('overlay-container', OverlayContainer);
