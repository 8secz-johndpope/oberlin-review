"use strict";

/*
 * Special event for image load events
 * Needed because some browsers does not trigger the event on cached images.

 * MIT License
 * Paul Irish     | @paul_irish | www.paulirish.com
 * Andree Hansson | @peolanha   | www.andreehansson.se
 * 2010.
 *
 * Usage:
 * $(images).bind('load', function (e) {
 *   // Do stuff on load
 * });
 * 
 * Note that you can bind the 'error' event on data uri images, this will trigger when
 * data uri images isn't supported.
 * 
 * Tested in:
 * FF 3+
 * IE 6-8
 * Chromium 5-6
 * Opera 9-10
 */
// (function ($) {
// 	$.event.special.load = {
// 		add: function (hollaback) {
// 			if ( this.nodeType === 1 && this.tagName.toLowerCase() === 'img' && this.src !== '' ) {
// 				// Image is already complete, fire the hollaback (fixes browser issues were cached
// 				// images isn't triggering the load event)
// 				if ( this.complete || this.readyState === 4 ) {
// 					hollaback.handler.apply(this);
// 				}
// 
// 				// Check if data URI images is supported, fire 'error' event if not
// 				else if ( this.readyState === 'uninitialized' && this.src.indexOf('data:') === 0 ) {
// 					$(this).trigger('error');
// 				}
// 				
// 				else {
// 					$(this).bind('load', hollaback.handler);
// 				}
// 			}
// 		}
// 	};
// }(jQuery));

// JAVASCRIPT REFACTOR

(function(){
	
	var review = window.review = {},
		overlay = review.overlay = {},
		photos = review.photos = {},
		twitter = review.twitter = {},
		comments = review.comments = {},
		galleries = review.galleries = {},
		slideshows = review.slideshows = {};
			
		/* Twitter
		-------------------------------------------------- */
		
		twitter.setup = function () {
			var request = $.getJSON('http://twitter.com/statuses/user_timeline/oberlinreview.json?count=1&callback=?',
				function(response){
					// put the most recent tweet into the twitter box
					$('#twitter p').eq(0).html(response[0].text);
					// make the twitter text a faux link to the twitter page
					$('#twitter').click(function(){window.location = 'http://twitter.com/oberlinreview';});
					// make the cursor act as though it's a link
					$('#twitter').css('cursor','pointer');
				}
			);
		}
		
		/* Comments
		-------------------------------------------------- */
		comments.setup = function () {
			var preview = $('<div class="comment"><p><b>Comment Preview:</b> <a id="publishbutton" style="float:right" href="#">publish comment</a></p><div id="commenttext"><p style="color:#BBB">Your comment can go here!</p></div><p class="userline"><span style="color:#BBB">&#8212; Your Name</span></p></div>'),
				namefield = $('#id_name'),
				emailfield = $('#id_email'),
				urlfield = $('#id_url'),
				commentfield = $('#id_comment'),
				showdown = new Showdown.converter(),
				update_name = function () {
					if(namefield.val() != '' && urlfield.val() == ''){
						$('.userline', preview).eq(0).html('&#8212; <b>' + namefield.val() + '</b>');
					}else if(namefield.val() != '' && urlfield.val() != ''){
						$('.userline', preview).eq(0).html('&#8212; <a href="' + urlfield.val() + '">' + namefield.val() + '</a>');
					}else{
						$('.userline', preview).eq(0).html('<span style="color:#BBB">&#8212; Your Name</span>')
					}
					$('#comments').masonry({ columnWidth: 360, singleMode: true });
				},
				update_comment = function () {
					if(commentfield.val() != ''){
						var html = showdown.makeHtml(commentfield.val());
						$('#commenttext').html(html);
					}else{
						$('#commenttext').html('<p style="color:#BBB">Your comment can go here!</p>');
					}
					$('#comments').masonry({ columnWidth: 360, singleMode: true });
				},
				submit_comment = function () {
					$('#commentform').submit();
				};

			$('#comments').append(preview);

			// When someone clicks on the preview, focus on the form	
			preview.click(function(){$('#id_name').focus()});

			// When someone updates the fields, update the preview
			namefield.keyup(update_name);
			urlfield.keyup(update_name);
			commentfield.keyup(update_comment);
			$('#publishbutton').click(submit_comment);

			// setup masonry on the comments for a much nicer flow than floats
			$('#comments').masonry({ columnWidth: 360, singleMode: true });
		}

		/* Overlay
		-------------------------------------------------- */

		overlay.backdrop = overlay.bd = $('<div id="lbbd"></div>');
		overlay.box = overlay.bx = $('<div id="lbbox"></div>');
		overlay.setup = function () {
			var bd = overlay.backdrop,
				bx = overlay.box,
				$body = $(document.body);
			
			// put the two overlay divs in the body
			$body.append(bd);
			$body.append(bx);
			// hide them both
			bd.hide();
			bx.hide();
			// add a click event to the backdrop
			bd.click(overlay.hide);
			// resize the overlay on window resize
			$(window).resize(overlay.fill_with_current_dimensions);
		};
		overlay.show = overlay.open = function () {
			overlay.bd.fadeIn();
			overlay.bx.fadeIn();
		};
		overlay.hide = overlay.close = function () {
			overlay.bx.fadeOut({
				complete: function () {
					overlay.bd.fadeOut();
					overlay.trigger_close_event();
				}
			});
		};
		overlay.empty = function () {
			overlay.box.html('');
		};
		overlay.append = function (el) {
			$(overlay.bx).append(el);
		};
		overlay.fill = function (x_max, y_max) {
			var $window = $(window),
				dimensions;
			overlay.x_max = x_max;
			overlay.y_max = y_max;
			dimensions = overlay.calculate_dimensions(x_max, y_max, $window.width()-40, $window.height()-40);
			overlay.bx.css({'width':dimensions.x,'height':dimensions.y,'margin-left':-(dimensions.x+20)/2,'margin-top':-(dimensions.y+20)/2});
			overlay.trigger_resize_event();
			return dimensions;
		};
		overlay.fill_with_current_dimensions = function () {
			return overlay.fill(overlay.x_max, overlay.y_max);
		};
		overlay.animate_to_fill = function (x_max, y_max, callback) {
			var dimensions,
				$window = $(window),
				cb = callback || (function () {});
			overlay.x_max = x_max;
			overlay.y_max = y_max;
			dimensions = overlay.calculate_dimensions(x_max, y_max, $window.width()-40, $window.height()-40);
			overlay.bx.animate({'width':dimensions.x,'height':dimensions.y,'margin-left':-(dimensions.x+20)/2,'margin-top':-(dimensions.y+20)/2}, {complete:cb, step: overlay.trigger_resize_event});
			overlay.trigger_resize_event();
			return dimensions;
		};
		overlay.calculate_dimensions = function (o_width, o_height, max_width, max_height){
			var width, height;
			if(o_width < max_width && o_height < max_height){
				width = o_width;
				height = o_height;
			}else if(o_width < max_width && o_height > max_height){
				height = max_height;
				width = height*(o_width/o_height);
			}else if(o_width > max_width && o_height < max_height){
				width = max_width;
				height = width*(o_height/o_width);
			}else if(o_width > max_width && o_height > max_height){
				width = max_width;
				height = width*(o_height/o_width);
				if(height > max_height){
					height = max_height;
					width = height*(o_width/o_height);
				}
			}
			return {x:width,y:height};
		};
		overlay.dimensions = function () {
			var w = overlay.bx.width(),
				h = overlay.bx.height();
			return {x: w, y: h};
		}
		overlay.trigger_resize_event = function () {
			overlay.bx.trigger('resize');
		};
		overlay.trigger_close_event = function () {
			overlay.bx.trigger('close');
		}
		overlay.loading = function () {
			overlay.bx.addClass('loading');
		};
		overlay.notloading = function () {
			overlay.bx.removeClass('loading');
		}
		
		/* Photos
		-------------------------------------------------- */

		photos.setup = function () {
			var lblinks,
				imglks = photos.image_links = lblinks = $("a[href$='.png'], a[href$='.jpg'], a[href$='.gif']");
			
			imglks.click(photos.show);
		};
		photos.show = function (e) {
			var $this = $(this),
				url = $this.attr('href'),
				// create an image element
				lkimg = $('<img src="'+url+'" />').css('opacity',0);
			

			// prevent the link from going anywhere
			e.preventDefault();
			// empty the lightbox if it isn't already
			overlay.empty();
			// open up the lightbox
			overlay.show();
			// add the loading class
			overlay.loading();
			// append the linkimg
			overlay.append(lkimg);
			// add the load event
			lkimg.load(function(){
				var $this = $(this),
					w = $this.width(),
					h = $this.height(),
					dim = overlay.animate_to_fill(w,h, function () {$this.animate({'opacity': 1});});
				$this.height(dim.y);
				$this.width(dim.x);
				// remove the loading class
				overlay.notloading();
				// add a close event to clicking on the photo
				$this.click(overlay.hide);
				// bind an event to resize the photo when the lightbox resizes
				overlay.bx.bind('resize.photo',function () {
					var dim = overlay.dimensions();
					$this.height(dim.y);
					$this.width(dim.x);
				});
				// bind an event to unbind the previous event when the lightbox closes
				overlay.bx.bind('close.photo', function () {
					overlay.empty();
					overlay.bx.unbind('resize.photo');
					overlay.bx.unbind('close.photo');
				});
			});
		}

		/* Slideshows
		-------------------------------------------------- */
		slideshows.setup = function () {
			var gallerylinks = slideshows.gallerylinks = $('a[href*="/gallery/"]');
			gallerylinks.click(slideshows.start);
		};
		slideshows.start = function(e) {
			var $this = $(this),
				href = $this.attr('href'),
				// strip the trailing / and add .slideshow
				sshowlink = href.substring(href.indexOf('/gallery'), href.length-1) + '.slideshow';
			e.preventDefault();
			
			$.getJSON(sshowlink, {data:'data'}, slideshows.render);
			
			// empty, show, and add the loading class to the overlay
			overlay.empty();
			overlay.show();
			overlay.loading();
			overlay.bx.bind('close.slideshow', function(){
				overlay.bx.unbind('mouseover.slideshow');
				overlay.bx.unbind('mouseout.slideshow');
				overlay.bx.unbind('resize.slideshow');
				overlay.bx.unbind('close.slideshow');
			});
		};
		slideshows.render = function(d, s, x){
			var i, html;
			slideshows.container = $('<div id="ssall"></div>');
			slideshows.stage = $('<div id="ssstage"></div>');
			slideshows.next = $('<div id="ssnext">»</div>').css('opacity',0).click(slideshows.next_slide);
			slideshows.prev = $('<div id="ssprev">«</div>').css('opacity',0).click(slideshows.prev_slide);
			
			slideshows.container.append(slideshows.stage);
			overlay.append(slideshows.next);
			overlay.append(slideshows.prev);
			overlay.append(slideshows.container);
			overlay.bx.bind('mouseover.slideshow', slideshows.show_controls);
			overlay.bx.bind('mouseout.slideshow', slideshows.hide_controls);
			
			slideshows.images = d.images;
			for (i=0; i < slideshows.images.length; i++) {
				html = [
					'<div class="ssimage">',
					'<img src="',slideshows.images[i].full,'" />',
					'<div class="sscaption"><b class="title">',slideshows.images[i].title,'</b>',slideshows.images[i].caption,'</div>',
					'</div>'
				].join('')
				slideshows.images[i].el = $(html).hide();
				overlay.append(slideshows.images[i].el);
			}
			
			
			slideshows.current = -1;
			slideshows.length = slideshows.images.length;
			slideshows.next_slide();
		};
		slideshows.next_slide = function () {
			overlay.bx.unbind('resize.slideshow');
			overlay.loading();
			if(slideshows.images[slideshows.current]){
				slideshows.images[slideshows.current].el.fadeOut();
			}
			slideshows.current = (1 + slideshows.current) % slideshows.length;
			slideshows.images[slideshows.current].el.show().css('opacity',0);
			$('img', slideshows.images[slideshows.current].el).load(slideshows.render_image);
			setTimeout($.proxy(slideshows.render_image, $('img', slideshows.images[slideshows.current].el)),1000);
		};
		slideshows.prev_slide = function () {
			overlay.bx.unbind('resize.slideshow');
			overlay.loading();
			if(slideshows.images[slideshows.current]){
				slideshows.images[slideshows.current].el.fadeOut();
			}
			slideshows.current = (slideshows.current - 1 + slideshows.length) % slideshows.length;
			slideshows.images[slideshows.current].el.show().css('opacity',0);
			$('img', slideshows.images[slideshows.current].el).load(slideshows.render_image);
			setTimeout($.proxy(slideshows.render_image, $('img', slideshows.images[slideshows.current].el)),1000);
		}
		slideshows.render_image = function () {
			var $img = $(this),
				$slide = $img.parent(),
				dim;
				
				$img.width('auto').height('auto');
				
				dim = overlay.animate_to_fill($img.width(), $img.height(), function () {
					slideshows.resize_image();
					$slide.animate({'opacity':1});
					slideshows.show_controls();
					overlay.notloading();
					overlay.bx.bind('resize.slideshow', slideshows.resize_image);
				});
		};
		slideshows.show_controls = function () {
			if(slideshows.controls) return;
			slideshows.controls = true;
			$('.sscaption, #ssnext, #ssprev').stop();
			$('.sscaption, #ssnext, #ssprev').animate({opacity:1}, 250);
		};
		slideshows.hide_controls = function () {
			if(!slideshows.controls) return;
			slideshows.controls = false;
			$('.sscaption, #ssnext, #ssprev').stop();
			$('.sscaption, #ssnext, #ssprev').animate({opacity:0}, 250);
		};
		slideshows.resize_image = function () {
			var dim = overlay.dimensions();
			$('img',slideshows.images[slideshows.current].el).height(dim.y).width(dim.x);
		}
		
		/* Galleries
		-------------------------------------------------- */
		galleries.setup = function () {
			var thumbs = $('.wings li a'),
				stage = $('.stage'),
				stage_img = $('img', stage),
				stage_byline = $('.byline', stage),
				stage_title = $('.headline', stage),
				stage_caption = $('.caption', stage),
				switch_image = function (e) {
					var $this = $(this),
						$credit = $('.byline', $this).eq(0),
						$caption = $('.caption', $this).eq(0),
						$title = $('.headline', $this).eq(0),
						$guts = $('*', stage);
					e.preventDefault();
					// if the current image is the newly selected one, stop.
					if($this.attr('href')==stage_img.attr('src'))
						return;
					// this'll get us the loading graphic
					stage.addClass('loading');
					// otherwise, fade out everything on stage
					$guts.fadeOut('fast', function () {
						stage_img.attr('src',$this.attr('href'));
						stage_byline.html($credit.html());
						stage_title.html($title.html());
						stage_caption.html($caption.html());
					});
				},
				image_fade_in = function (e) {
					var $this = $(this),
						$guts = $('*', stage),
						stageheight;
						
					$guts.show();
					stageheight = stage_byline.outerHeight()+Math.max(stage_title.outerHeight(), stage_caption.outerHeight()) + stage_img.outerHeight();
					$guts.hide();
					stage.animate({'height':stageheight},
						function () {
							$guts.fadeIn('fast');
							stage.removeClass('loading');
						}
					);
				};
			// unbind the normal photo zoom behavior
			thumbs.unbind();
			thumbs.click(switch_image);
			stage_img.load(image_fade_in);
		};
		
		/* Setup Scripts
		-------------------------------------------------- */
		//$(twitter.setup);
		$(comments.setup);
		$(overlay.setup);
		$(photos.setup);
		$(slideshows.setup);
		$(galleries.setup);
		$(function(){
			$('.drop > a').bind('click', function(e){
				var $drop = $(this).parent();
				$('.drop.active').not($drop).removeClass('active'); // disable all other active dropdowns
				$drop.toggleClass('active'); // toggle the clicked dropdown
				e.preventDefault(); // prevent the link from following
			});
			$('.drop > a').dblclick(function(e){
				var $this = $(this);
				window.location = $this.eq(0).attr('href');
			});
		});
}());