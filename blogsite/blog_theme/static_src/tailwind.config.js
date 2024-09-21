module.exports = {
    darkMode : "class",

    content: [
        '../templates/**/*.html',
        '../blog_theme/templates/**/*.html',
        '../../home/templates/**/*.html',
        // Add any additional paths if necessary
    ],
    theme: {
        extend: {
            screens:{
                "sm": "480px",
                "md": "768px",
                "lg": "1024px",
                "xl": "1280px",
            }
        },
        fontfamily: {
            nunito: ['Nunito', 'sans-serif'],
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
