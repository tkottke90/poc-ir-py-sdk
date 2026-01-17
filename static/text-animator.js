/**
 * TextAnimator - Handles cycling through HTML elements with entrance/exit animations
 */
export class TextAnimator {
  /**
   * @param {HTMLElement[]} elements - Array of HTML elements to animate
   * @param {number} displayDuration - How long each element is shown (in milliseconds)
   * @param {Object} options - Optional configuration
   * @param {number} options.enterDuration - Duration of enter animation in ms (default: 600)
   * @param {number} options.exitDuration - Duration of exit animation in ms (default: 800)
   */
  constructor(elements, displayDuration, options = {}) {
    if (!elements || elements.length === 0) {
      throw new Error('TextAnimator requires at least one element');
    }

    this.elements = elements;
    this.displayDuration = displayDuration;
    this.enterDuration = options.enterDuration || 600;
    this.exitDuration = options.exitDuration || 800;
    this.currentIndex = 0;
    this.isRunning = false;
    this.timeoutId = null;

    // Hide all elements initially
    this.elements.forEach(el => {
      el.style.opacity = '0';
      el.style.position = 'absolute';
    });
  }

  /**
   * Start the animation loop
   */
  start() {
    if (this.isRunning) {
      return;
    }

    this.isRunning = true;
    this.showElement(this.currentIndex);
  }

  /**
   * Stop the animation loop
   */
  stop() {
    this.isRunning = false;
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
      this.timeoutId = null;
    }
  }

  /**
   * Reset to the first element
   */
  reset() {
    this.stop();
    this.currentIndex = 0;
    this.elements.forEach(el => {
      el.classList.remove('text-enter', 'text-exit');
      el.style.opacity = '0';
    });
  }

  /**
   * Show a specific element with entrance animation
   * @param {number} index - Index of element to show
   */
  showElement(index) {
    if (!this.isRunning) {
      return;
    }

    const element = this.elements[index];
    
    // Remove any existing animation classes
    element.classList.remove('text-exit');
    
    // Trigger entrance animation
    element.classList.add('text-enter');

    // Schedule the exit animation
    this.timeoutId = setTimeout(() => {
      this.hideElement(index);
    }, this.displayDuration);
  }

  /**
   * Hide the current element with exit animation and show the next one
   * @param {number} index - Index of element to hide
   */
  hideElement(index) {
    if (!this.isRunning) {
      return;
    }

    const element = this.elements[index];
    
    // Remove entrance class and add exit class
    element.classList.remove('text-enter');
    element.classList.add('text-exit');

    // Calculate next index
    const nextIndex = (index + 1) % this.elements.length;
    this.currentIndex = nextIndex;

    // Wait for exit animation to complete before showing next element
    this.timeoutId = setTimeout(() => {
      // Clean up the exited element
      element.classList.remove('text-exit');
      element.style.opacity = '0';
      
      // Show next element
      this.showElement(nextIndex);
    }, this.exitDuration);
  }

  /**
   * Get the currently visible element index
   * @returns {number}
   */
  getCurrentIndex() {
    return this.currentIndex;
  }

  /**
   * Update the display duration
   * @param {number} duration - New duration in milliseconds
   */
  setDisplayDuration(duration) {
    this.displayDuration = duration;
  }
}

