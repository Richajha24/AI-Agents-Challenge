/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
    theme: {
        extend: {
            colors: {
                navy: "#0B1324",
                ivory: "#F5F1E6",
                graphite: "#2F2F2F",
                gold: "#C9A24C",
            },
            boxShadow: {
                soft: "0 10px 30px rgba(0,0,0,0.25)",
            },
        },
    },
    plugins: [],
};

