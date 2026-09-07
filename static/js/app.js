document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "DOK-ANPR interface initialized."
        );


        /*
         * Highlight current navigation item
         */

        const currentPath =
            window.location.pathname;

        document
            .querySelectorAll(".nav-link")
            .forEach(function (link) {

                const href =
                    link.getAttribute("href");

                if (
                    href &&
                    href !== "#" &&
                    currentPath === href
                ) {

                    link.classList.add(
                        "active"
                    );

                }

            });


        /*
         * File upload preview
         */

        const fileInput =
            document.querySelector(
                'input[type="file"]'
            );

        if (fileInput) {

            fileInput.addEventListener(
                "change",
                function () {

                    if (
                        this.files &&
                        this.files.length > 0
                    ) {

                        console.log(
                            "Selected video:",
                            this.files[0].name
                        );

                    }

                }
            );

        }

    }
);