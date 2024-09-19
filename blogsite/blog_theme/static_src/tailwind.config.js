module.exports = {
    content: [
        '../templates/**/*.html',
        '../blog_theme/templates/**/*.html',
        '../../home/templates/**/*.html',
        // Add any additional paths if necessary
    ],
    theme: {
        extend: {
            screens:{
                "sm": "480px"
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
