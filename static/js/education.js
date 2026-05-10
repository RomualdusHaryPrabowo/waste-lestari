/**
 * EcoSort AI — Education Page JavaScript
 * Category card animations
 */

document.addEventListener('DOMContentLoaded', () => {
    // Add animation delay to category cards
    const cards = document.querySelectorAll('.category-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
});