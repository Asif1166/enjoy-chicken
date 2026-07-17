/* ===================================================================
    
    Author          : Valid Theme
    Template Name   : Restan - Food & Restaurant HTML Template 
    Version         : 1.0
    
* ================================================================= */
(function($) {
	"use strict";

	$(document).ready(function() {

		/* ==================================================
		    # Tooltip Init
		===============================================*/
		$('[data-toggle="tooltip"]').tooltip();


		/* ==================================================
		    # Youtube Video Init
		 ===============================================*/
		$('.player').mb_YTPlayer();


		/* ==================================================
		    # Scrolla active
		===============================================*/
		$('.animate').scrolla({
			// default
			mobile: false, // disable animation on mobiles
		});


		/* ==================================================
		    # imagesLoaded active
		===============================================*/
		$('#gallery-masonary,.blog-masonry').imagesLoaded(function() {

			/* Filter menu */
			$('.mix-item-menu').on('click', 'button', function() {
				var filterValue = $(this).attr('data-filter');
				$grid.isotope({
					filter: filterValue
				});
			});

			/* filter menu active class  */
			$('.mix-item-menu button').on('click', function(event) {
				$(this).siblings('.active').removeClass('active');
				$(this).addClass('active');
				event.preventDefault();
			});

			/* Filter active */
			var $grid = $('#gallery-masonary').isotope({
				itemSelector: '.gallery-item',
				percentPosition: true,
				masonry: {
					columnWidth: '.gallery-item',
				}
			});

			/* Filter active */
			$('.blog-masonry').isotope({
				itemSelector: '.blog-item',
				percentPosition: true,
				masonry: {
					columnWidth: '.blog-item',
				}
			});

		});


		/* ==================================================
		    # Fun Factor Init
		===============================================*/
		$('.timer').countTo();
		$('.fun-fact').appear(function() {
			$('.timer').countTo();
		}, {
			accY: -100
		});
		

		/* ==================================================
		    # Magnific popup init
		 ===============================================*/
		$(".popup-link").magnificPopup({
			type: 'image',
			// other options
		});

		$(".popup-gallery").magnificPopup({
			type: 'image',
			gallery: {
				enabled: true
			},
			// other options
		});

		$(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
			type: "iframe",
			mainClass: "mfp-fade",
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false
		});

		$('.magnific-mix-gallery').each(function() {
			var $container = $(this);
			var $imageLinks = $container.find('.item');

			var items = [];
			$imageLinks.each(function() {
				var $item = $(this);
				var type = 'image';
				if ($item.hasClass('magnific-iframe')) {
					type = 'iframe';
				}
				var magItem = {
					src: $item.attr('href'),
					type: type
				};
				magItem.title = $item.data('title');
				items.push(magItem);
			});

			$imageLinks.magnificPopup({
				mainClass: 'mfp-fade',
				items: items,
				gallery: {
					enabled: true,
					tPrev: $(this).data('prev-text'),
					tNext: $(this).data('next-text')
				},
				type: 'image',
				callbacks: {
					beforeOpen: function() {
						var index = $imageLinks.index(this.st.el);
						if (-1 !== index) {
							this.goTo(index);
						}
					}
				}
			});
		});


		/* ==================================================
		    _Progressbar Init
		 ===============================================*/
		function animateElements() {
			$('.progressbar').each(function() {
				var elementPos = $(this).offset().top;
				var topOfWindow = $(window).scrollTop();
				var percent = $(this).find('.circle').attr('data-percent');
				var animate = $(this).data('animate');
				if (elementPos < topOfWindow + $(window).height() - 30 && !animate) {
					$(this).data('animate', true);
					$(this).find('.circle').circleProgress({
						// startAngle: -Math.PI / 2,
						value: percent / 100,
						size: 130,
						thickness: 13,
						lineCap: 'round',
						emptyFill: '#f1f1f1',
						fill: {
							gradient: ['#2667FF', '#6c19ef']
						}
					}).on('circle-animation-progress', function(event, progress, stepValue) {
						$(this).find('strong').text((stepValue * 100).toFixed(0) + "%");
					}).stop();
				}
			});

		}

		animateElements();
		$(window).scroll(animateElements);


		/* ==================================================
            # Banner Carousel
         ===============================================*/
		const bannerFade = new Swiper(".banner-fade", {
			// Optional parameters
			direction: "horizontal",
			loop: true,
			autoplay: true,
			effect: "fade",
			fadeEffect: {
				crossFade: true
			},
			speed: 3000,
			autoplay: {
				delay: 5000,
				disableOnInteraction: false,
			},

			// If we need pagination
			pagination: {
				el: '.swiper-pagination',
				type: 'bullets',
				clickable: true,
			},

			// Navigation arrows
			navigation: {
				nextEl: ".swiper-button-next",
				prevEl: ".swiper-button-prev"
			}

			// And if we need scrollbar
			/*scrollbar: {
            el: '.swiper-scrollbar',
          },*/
		});


		/* ==================================================
            # Brand Carousel
         ===============================================*/
		 const brandCarousel = new Swiper(".brand-style-one-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 2,
			spaceBetween: 30,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			// Navigation arrows
			navigation: {
				nextEl: ".swiper-button-next",
				prevEl: ".swiper-button-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 3,
					spaceBetween: 30,
				},
				992: {
					slidesPerView: 4,
					spaceBetween: 30,
				},
				1400: {
					slidesPerView: 5,
					spaceBetween: 30,
				}
			},
		});


		/* ==================================================
            # Food Category Carousel
         ===============================================*/
		 const foodCatCarousel = new Swiper(".food-cat-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			// Navigation arrows
			navigation: {
				nextEl: ".food-cat-next",
				prevEl: ".food-cat-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					spaceBetween: 30,
				},
				992: {
					slidesPerView: 3,
					spaceBetween: 30,
				}
			},
		});


		/* ==================================================
            # Gallery Carousel
         ===============================================*/
		const galleryCarousel = new Swiper(".gallery-style-one-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 50,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			breakpoints: {
				778: {
					slidesPerView: 2,
				},
				1200: {
					slidesPerView: 2.5,
					centeredSlides: true,
				},
			},
		});


		/* ==================================================
            # Testimonials Carousel
         ===============================================*/
		const testimonialCarousel = new Swiper(".testimonial-carousel", {
			// Optional parameters
			direction: "horizontal",
			loop: true,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},

			// And if we need scrollbar
			/*scrollbar: {
            el: '.swiper-scrollbar',
          },*/
		});


		/* ==================================================
            # Food Menu Carousel
         ===============================================*/
		 const foodMenuCarousel = new Swiper(".food-menu-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: false,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			// Navigation arrows
			navigation: {
				nextEl: ".swiper-button-next",
				prevEl: ".swiper-button-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					spaceBetween: 30,
				},
				992: {
					slidesPerView: 3,
					spaceBetween: 30,
				},
				1400: {
					slidesPerView: 4,
					spaceBetween: 30,
				},
			},
		});


		/* ==================================================
            # Services Style One Carousel
         ===============================================*/
		 const testimonialTwo = new Swiper(".services-style-one-carousel", {
			// Optional parameters
			loop: true,
			freeMode: true,
			grabCursor: true,
			slidesPerView: 1,
			spaceBetween: 50,
			autoplay: true,
			pagination: {
				el: ".swiper-pagination",
				clickable: true,
			},
			navigation: {
				nextEl: ".services-cat-next",
				prevEl: ".services-cat-prev"
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				1200: {
					slidesPerView: 3,
				},
			},
		});
		

		/* ==================================================
            # Product Gallery Carousel
         ===============================================*/
		 const productGallery = new Swiper(".product-gallery-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 2,
			spaceBetween: 30,
			autoplay: false,
			breakpoints: {
				768: {
					slidesPerView: 3,
				},
				992: {
					slidesPerView: 3,
				},
				1200: {
					slidesPerView: 4,
				},
			},
		});


		/* ==================================================
            # Related Product Carousel
         ===============================================*/
		 const relatedProduct = new Swiper(".related-product-carousel", {
			// Optional parameters
			loop: true,
			slidesPerView: 1,
			spaceBetween: 30,
			autoplay: true,
			breakpoints: {
				768: {
					slidesPerView: 2,
				},
				992: {
					slidesPerView: 3,
				},
				1400: {
					slidesPerView: 4,
				},
			},
		});


		/* ==================================================
		    Date Picker Init
		================================================== */
		$('.date-picker-one').datepicker()

		/* ==================================================


		Nice Select Init
		===============================================*/
		$('.reservation-form select').niceSelect();


		/* ==================================================
		    GSAP animation
		================================================== */

		let animateUpDown = document.querySelector(".upDownScrol");
		if (animateUpDown) {

			gsap.set(".upDownScrol", {
				yPercent: 105
			});
			gsap.to(".upDownScrol", {
				yPercent: -105,
				ease: "none",
				scrollTrigger: {
					trigger: ".upDownScrol",
					end: "bottom center",
					scrub: 1
				},
			});
		}


		/* ==================================================
		    Contact Form Validations
		================================================== */
		$('.contact-form').each(function() {
			var formInstance = $(this);
			formInstance.submit(function() {

				var action = $(this).attr('action');

				$("#message").slideUp(750, function() {
					$('#message').hide();

					$('#submit')
						.after('<img src="assets/img/ajax-loader.gif" class="loader" />')
						.attr('disabled', 'disabled');

					$.post(action, {
							name: $('#name').val(),
							email: $('#email').val(),
							phone: $('#phone').val(),
							comments: $('#comments').val()
						},
						function(data) {
							document.getElementById('message').innerHTML = data;
							$('#message').slideDown('slow');
							$('.contact-form img.loader').fadeOut('slow', function() {
								$(this).remove()
							});
							$('#submit').removeAttr('disabled');
						}
					);
				});
				return false;
			});
		});

	}); // end document ready function


	/* ==================================================
        Preloader Init
     ===============================================*/
	 function loader() {
		$(window).on('load', function() {
			$('#restan-preloader').addClass('loaded');
			$("#loading").fadeOut(500);
			// Una vez haya terminado el preloader aparezca el scroll

			if ($('#restan-preloader').hasClass('loaded')) {
				// Es para que una vez que se haya ido el preloader se elimine toda la seccion preloader
				$('#preloader').delay(900).queue(function() {
					$(this).remove();
				});
			}
		});
	}
	loader();



})(jQuery); // End jQuery










document.addEventListener('DOMContentLoaded', function() {
    // Select all quantity-edit divs
    const quantityEdits = document.querySelectorAll('.quantity-edits');
    
    // Function to update subtotal and total
    const updateCartTotals = () => {
        let totalCartAmount = 0;
        
        quantityEdits.forEach((edit) => {
            const inputField = edit.querySelector('.input');
            const price = parseFloat(edit.closest('tr').querySelector('.product-item-price').innerText.replace('€', '').trim());
            const subtotalField = edit.closest('tr').querySelector('.product-item-totle span');
            
            // Calculate the subtotal for this row
            const quantity = parseInt(inputField.value);
            const subtotal = quantity * price;
            subtotalField.innerText = subtotal.toFixed(2);
            
            // Add to the total cart amount
            totalCartAmount += subtotal;
        });

        // Update the total cart amount in the DOM
        document.querySelector('.cart_total').innerText = totalCartAmount.toFixed(2);
    };
    
    // Loop through each quantity-edit div and add event listeners
    quantityEdits.forEach((edit) => {
        const inputField = edit.querySelector('.input');
        const plusButton = edit.querySelector('.plus');
        const minusButton = edit.querySelector('.minus');
        
        // Add event listener for the plus button
        plusButton.addEventListener('click', () => {
            inputField.value = parseInt(inputField.value) + 1;
            updateCartTotals();
        });
        
        // Add event listener for the minus button
        minusButton.addEventListener('click', () => {
            if (parseInt(inputField.value) > 1) { // Ensures the quantity doesn't go below 1
                inputField.value = parseInt(inputField.value) - 1;
                updateCartTotals();
            }
        });
    });

    // Initial call to set totals on page load
    updateCartTotals();
});


	





$(document).ready(function() {
    // Close modal function
    $(document).on('click', '.close-btn', function() {
        $('#addToCartModal').fadeOut();
    });

    // AJAX call
    $(document).off('click', '.add-to-cart-btn').on('click', '.add-to-cart-btn', function() {
        let this_val = $(this);
        let index = this_val.attr("data-index");
        let quantity = this_val.closest('.single-product-contents').find('.product-quantity-' + index).val();
        let product_title = $(".product-title-" + index).val();
        let product_id = $(".product-id-" + index).val();
        let product_price = this_val.closest('.single-product-contents').find('.currrent-product-price-' + index).text();
        let product_pid = $(".product-pid-" + index).val();
        
        // Get image if exists, otherwise use empty string
        let product_image = $(".product-image-" + index).val() || '';

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'qty': quantity,
                'title': product_title,
                'price': product_price,
                'image': product_image,
            },
            dataType: 'json',
            beforeSend: function() {
                console.log("Adding Product to cart...");
            },
            success: function(response) {
                console.log("Added Product to Cart!");

                // Update the cart count dynamically
                $(".cart-items-count .cart-count").text(response.totalcartitems);

                // Show modal with product title
                $('#modal-message').html(`Vous venez d'ajouter «<strong>${product_title}</strong>» à votre panier.`);
                $('#addToCartModal').fadeIn();
            }
        });
    });
});


  
  
  
  $(document).ready(function() {
	// Remove any previously attached event handlers to avoid double firing
	$(document).off('click', '.add-to-wishlist').on('click', '.add-to-wishlist', function() {
		let this_val = $(this);
		let index = this_val.attr("data-index");
  
		let product_title = $(".product-title-" + index).val();
		let product_id = $(".product-id-" + index).val();
		let product_pid = $(".product-pid-" + index).val();
		let product_image = $(".product-image-" + index).val();
  
		console.log("Product Title:", product_title);
		console.log("Product ID:", product_id);
		console.log("Product PID:", product_pid);
		console.log("Product Image:", product_image);
		console.log("Index:", index);
		console.log("Current Element:", this_val);
  
		$.ajax({
			url: '/add-to-wishlist',
			data: {
				'id': product_id,
				'pid': product_pid,
				'image': product_image,
				'title': product_title,
			},
			dataType: 'json',
			beforeSend: function() {
				console.log("Adding Product to Wishlist...");
			},
			success: function(response) {
				this_val.html("❤️"); // Change the icon or text after adding to wishlist
				console.log("Added Product to Wishlist!");
  
				// Update the wishlist count dynamically
				if (response.totalwishlistitems !== undefined) {
					$(".wishlist-items-count .wishlist-count").text(response.totalwishlistitems);
				} else {
					console.error("Error: Response does not contain 'totalwishlistitems'");
				}
			},
			error: function(xhr, status, error) {
				console.error("AJAX Error:", error);
			}
		});
	});
  });
  
  
  
  
  $(document).on('click', '.delete-product', function(){
	let product_id = $(this).attr("data-product")
	let this_val = $(this)
  
	console.log("Product Id:", product_id);
  
	$.ajax({
	  url: "/delete-from-cart",
	  data: {
		"id": product_id
	  },
	  dataType: "json",
	  beforeSend: function(){
		this_val.hide()
	  },
	  success: function(response){
		this_val.show()
		$(".cart-items-count").text(response.totalcartitems)
		$("#cart-list").html(response.data)
	  }
	})
  })
  
  
  
  $(document).on('click', '.delete-product-wishlist', function(){
	let product_id = $(this).attr("data-product");
	let this_val = $(this);
  
	console.log("Product Id:", product_id);
  
	$.ajax({
	  url: "/delete-from-wishlist",
	  data: {
		"id": product_id
	  },
	  dataType: "json",
	  beforeSend: function(){
		this_val.hide();
	  },
	  success: function(response){
		this_val.show();
		$(".wishlist-items-count").text(response.totalwishlistitems);
		$("#wishlist-list").html(response.data);
	  },
	  error: function(xhr, status, error) {
		console.log("Error:", error);
		this_val.show();  // Show the button again if there's an error
	  }
	});
  });
  
  

  function updateCartEvents() {
    // Detach any previous event listeners to prevent multiple bindings
    $(".button-wrapper-action .button").off('click').on('click', function() {
        let input = $(this).closest('.quantity-edit').find('.input');
        let currentValue = parseInt(input.val(), 10);
        if ($(this).hasClass('plus')) {
            input.val(currentValue + 1);
        } else {
            if (currentValue > 1) {
                input.val(currentValue - 1);
            }
        }
    });

    // Detach previous event listener for the update button
    $(".update-product").off('click').on('click', function() {
        let product_id = $(this).attr("data-product");
        let this_val = $(this);
        let product_quantity = $(".product-qty-" + product_id).val();

        console.log("Product Id:", product_id);
        console.log("Product qty:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity
            },
            dataType: "json",
            beforeSend: function() {
                this_val.hide();
            },
            success: function(response) {
                this_val.show();
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data);
                updateCartEvents(); // Reattach event listeners after updating the cart
            }
        });
    });
}

// Initial call to set up event listeners on page load
updateCartEvents();








document.addEventListener('DOMContentLoaded', function() {
	const translations = {
		'fr': {
			'track-order-link': 'Suivi de Commande',
			'currentlanguage': 'Français',
			'categories-text': 'Catégories',
			'category-text': 'Catégories',
			'my-cart-text': 'Mon Panier',
			'search-placeholder': 'Rechercher des produits, catégories ou marques',
			'search-button-text': 'Rechercher',
			'account-trans': 'Compte',
			'logout-trans': 'Déconnexion',
			'login-trans': 'Connexion',
			'signup-trans': 'S\'inscrire',
			'off-trans': 'de réduction',
			'JapaneseSushiText': 'Articles de Sushi Japonais',
			'MenuofferText': 'Offre Menu',
			'SpecialmenusText': 'Offre de menus spéciaux',
			'ChooseyourmenuText': 'Choisissez votre menu',
			'OurCartText': 'Notre Carte',
			'AboutusText': 'A propos de nous',
			'ReserveatableText': 'Réserver une table',

  
  
  
  
		},
		'en': {
			'track-order-link': 'Track Order',
			'currentlanguage': 'English',
			'categories-text': 'Categories',
			'category-text': 'Categories',
			'my-cart-text': 'My Cart',
			'search-placeholder': 'Search for products, categories or brands',
			'search-button-text': 'Search',
			'account-trans': 'Account',
			'logout-trans': 'Logout',
			'login-trans': 'Login',
			'signup-trans': 'Sign Up',
			'off-trans': 'Off',
			'JapaneseSushiText': 'Japanese Sushi items',
			'MenuofferText': 'Offer Menu',
			'SpecialmenusText': 'Special menus',
			'ChooseyourmenuText': 'Choose your menu',
			'OurCartText': 'Our Cart',
			'AboutusText': 'About us',
			'ReserveatableText': 'Reserve a table',

  
			
  
  
		}
	};





  // Function to change language
  function changeLanguage(lang) {
	const translation = translations[lang];
	if (translation) {
		// Update static elements
		const trackOrderLink = document.getElementById('track-order-link');
		const currentLanguage = document.getElementById('currentlanguage');
		const currentLanguageMobile = document.getElementById('currentlanguage-mobile');
		const categoriesText = document.getElementById('categories-text');
		const categoryText = document.getElementById('category-text');
		const myCartText = document.querySelector('.text');
		const searchPlaceholder = document.getElementById('search-placeholder');
		const searchButtonText = document.getElementById('search-button-text');
		const accountText = document.getElementById('account-trans');
		const logoutText = document.getElementById('logout-trans');
		const loginText = document.getElementById('login-trans');
		const signupText = document.getElementById('signup-trans');
		const offText = document.getElementById('off-trans');
		const JapaneseSushiText = document.getElementById('JapaneseSushiText');
		const MenuofferText = document.getElementById('MenuofferText');
		const SpecialmenusText = document.getElementById('SpecialmenusText');
		const ChooseyourmenuText = document.getElementById('ChooseyourmenuText');
		const OurCartText = document.getElementById('OurCartText');
		const AboutusText = document.getElementById('AboutusText');
		const ReserveatableText = document.getElementById('ReserveatableText');


		if (searchPlaceholder) searchPlaceholder.placeholder = translation['search-placeholder'];
		if (searchButtonText) searchButtonText.textContent = translation['search-button-text'];          
		if (myCartText) myCartText.textContent = translation['my-cart-text'];
		if (trackOrderLink) trackOrderLink.textContent = translation['track-order-link'];
		if (currentLanguage) currentLanguage.textContent = translation['currentlanguage'];
		if (currentLanguageMobile) currentLanguageMobile.textContent = translation['currentlanguage'];
		if (categoriesText) categoriesText.textContent = translation['categories-text'];
		if (categoryText) categoryText.textContent = translation['category-text'];
		if (accountText) accountText.textContent = translation['account-trans'];
		if (logoutText) logoutText.textContent = translation['logout-trans'];
		if (loginText) loginText.textContent = translation['login-trans'];
		if (signupText) signupText.textContent = translation['signup-trans'];
		if (offText) offText.textContent = translation['off-trans'];
		if (JapaneseSushiText) JapaneseSushiText.textContent = translation['JapaneseSushiText'];
		if (MenuofferText) MenuofferText.textContent = translation['MenuofferText'];
		if (SpecialmenusText) SpecialmenusText.textContent = translation['SpecialmenusText'];
		if (ChooseyourmenuText) ChooseyourmenuText.textContent = translation['ChooseyourmenuText'];
		if (OurCartText) OurCartText.textContent = translation['OurCartText'];
		if (AboutusText) AboutusText.textContent = translation['AboutusText'];
		if (ReserveatableText) ReserveatableText.textContent = translation['ReserveatableText'];

		// Update dynamic content for both desktop and mobile
		document.querySelectorAll('.nav-link').forEach(function(element) {
			const title = element.getAttribute(`data-title-${lang}`);
			if (title) {
				element.textContent = title;
			}
		});

		document.querySelectorAll('.sub-b, .mobile-menu-link').forEach(function(element) {
			const title = element.getAttribute(`data-title-${lang}`);
			if (title) {
				element.textContent = title;
			}
		});




		  // Update about section
		document.querySelectorAll('[data-title-fr]').forEach(function(element) {
			const title = element.getAttribute(`data-title-${lang}`);
			if (title) {
				element.textContent = title;
			}
		});

		document.querySelectorAll('[data-description-fr]').forEach(function(element) {
			const description = element.getAttribute(`data-description-${lang}`);
			if (description) {
				element.textContent = description;
			}
		});

		document.querySelectorAll('[data-button-text-fr]').forEach(function(element) {
			const buttonText = element.getAttribute(`data-button-text-${lang}`);
			if (buttonText) {
				element.textContent = buttonText;
			}
		});






		// Store selected language in session storage
		sessionStorage.setItem('selectedLanguage', lang);
	}
}

// Load the selected language from session storage or default to French
const selectedLanguage = sessionStorage.getItem('selectedLanguage') || 'fr';
changeLanguage(selectedLanguage);

// Add event listeners for both desktop and mobile language change
document.getElementById('lang-french').addEventListener('click', function(event) {
	event.preventDefault();
	changeLanguage('fr');
});

document.getElementById('lang-english').addEventListener('click', function(event) {
	event.preventDefault();
	changeLanguage('en');
});

document.getElementById('lang-french-mobile').addEventListener('click', function(event) {
	event.preventDefault();
	changeLanguage('fr');
});

document.getElementById('lang-english-mobile').addEventListener('click', function(event) {
	event.preventDefault();
	changeLanguage('en');
});
});

