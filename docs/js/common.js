/*
# Copyright 2018 Google Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/
// Youtube Player API
// create script tag and add to DOM
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

$('#project-id').on('input',  function() {
  var projectId = document.getElementById('project-id');
  var projectIdValue = projectId.value;
  var anchorTagId = projectId.getAttribute('data-target-id');
  var anchorTag = document.getElementById(anchorTagId);
  var launchTag = document.getElementById('crm-launch');

  /*
   * A project ID must be 6 to 30 lowercase letters, digits, or hyphens.
   * It must start with a letter and trailing hyphens are prohibited.
   */
  var projRe = /^[a-z][a-z0-9-]{4,28}[a-z0-9]$/;

  if (projRe.test(projectIdValue)) {
    var templateUrl = anchorTag.getAttribute('data-href');
    var re = /(.*project=)([^&]+)(.*)/;
    var matches = re.exec(templateUrl);
    var newUrl = [
      matches[1],
      projectIdValue,
      matches[3]
    ].join('');
    anchorTag.href = newUrl;
    anchorTag.classList.remove('gray-image');
    launchTag.href = 'https://' + projectIdValue + '.appspot.com';
    launchTag.innerHTML = projectIdValue + '.appspot.com';
  } else {
    anchorTag.removeAttribute('href');
    launchTag.removeAttribute('href');
    anchorTag.classList.add('gray-image');
    launchTag.innerHTML = '&lt;Project ID not set&gt;';
  }
});

$('#cloudshell-url').on('click',  function() {
  var cloudshellButton = document.getElementById('cloudshell-url');
  ga('send', 'event', 'docs', 'deployment', 'quickstart');
});

function createPlayer(key) {
  $('#player').append('<iframe id="ytplayer" type="text/html" width="640" height="390" src="https://www.youtube.com/embed/'+key+'" frameborder="0" allowfullscreen>');
}

// click event for presentations/talks in docs/talks
$('.pt').on('click', function() {
  var self = this;
  var video = $(self).data('key');

  createPlayer(video);

  resizePlayer();
  $('#player iframe').on('load', function() {
    $('.pt-lightbox').addClass('active');
  });
});


// Close lightbox when clicking anywhere on overlay
$('.pt-lightbox').on('click', function() {
  if ($(this).hasClass('active')) {
    $(this).removeClass('active');
    $(this).find('iframe').remove();
    $('body, html').removeClass('noscroll');
  }
});

// Resize Player
function resizePlayer() {
  var $inner = $('.pt-player'),
      defaultHeight = window.innerHeight || document.documentElement.clientHeight,
      defaultWidth = window.innerWidth || document.documentElement.clientWidth,
      maxHeight = defaultHeight*.75,
      maxWidth = defaultWidth*.75,
      newWidth = maxWidth,
      newHeight = 16 * maxWidth / 9;

  if (defaultWidth > defaultHeight){
      if (newHeight > maxHeight){
        newWidth = 16 * maxHeight / 9;
        newHeight = maxHeight;
      }
  } else {
      newWidth = 16 * maxHeight / 9;
      newHeight = maxHeight;
      if (newWidth > maxWidth){
          newHeight = 9 * maxWidth / 16;
          newWidth = maxWidth;
      }
  }

  $inner.css({"width": newWidth, "height": newHeight});
}



// Jquery UI for tabbed panes
$.getScript("https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js", function(){
  setupTabs();
});

// Add the 'external' class to every outbound link on the site.
// The css will add a small right arrow after the link.
$('a').filter(function() {
   return this.hostname && this.hostname !== location.hostname;
}).addClass("external");

//Set up tabs
function setupTabs(rootElement) {
      rootElement = rootElement || document;
      var tabs = $(rootElement).find('div.tabs');
      if(tabs.length > 0) {
        tabs.tabs();
      }
};

// Make the table of contents
$(document).ready(function() {
    var $window = $(window);

    // Sticky Nav on Scroll Up
    var iScrollPos = 0;

    $window.scroll(function () {
      var iCurScrollPos = $(this).scrollTop();
        if (iCurScrollPos > iScrollPos) {
          //Scrolling Down
          if ($('#sticky-nav').visible()){
            $('#sticky-nav').removeClass("on-page");
          }
        } else {
          //Scrolling Up
          if ($('.nav-hero-container').visible(true) && $('#sticky-nav').visible()){
            $('#sticky-nav').removeClass("on-page");
          } else if (!$('.nav-hero-container').visible(true)) {
            $('#sticky-nav').addClass("on-page");
          }
        }
        iScrollPos = iCurScrollPos;
    });

    $('.toc').click(function(){
      setTimeout(function(){
        $('#sticky-nav').addClass("on-page");
      }, 1000)
    });

    setTimeout(function(){
      if (document.URL.indexOf("#") != -1 && document.URL.indexOf("contribute") == -1 ) {
        $('#sticky-nav').addClass("on-page");
      }
    }, 1000);

    // Scroll to sections
    $('.btn-floating').on('click', function(){
      $('html, body').scrollTo(('#' +($(this).data("target"))), 350);
    })

    // Invoke slick JS carousel
    // Detailed documentation: http://kenwheeler.github.io/slick/
    $('.pt-container').slick({
      arrows: true,
      dots: false,
      autoplay: false,
      infinite: true,
      slidesToShow: 4,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            dots: false,
            arrows: true
          }
        },
        {
          breakpoint: 800,
          settings: {
            slidesToShow: 3,
            dots: true,
            arrows: false
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            dots: true,
            arrows: false
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            dots: true,
            arrows: false
          }
        }
      ]
    });

    $('.slick-next').on('click', function() {
      $('.slick-prev').addClass('active');
    });

    $('.toc').toc({ listType: 'ul' });

    $('.nav-toggle, .hamburger').on('click', function(){
      $('.top-nav').toggleClass('right');
    });

    $('.nav-doc-toggle').on('click', function(){
      $('.doc-list').toggleClass('active');
    });

    $(window).on('resize',function(){
       //send resize event to slick after it's been destroyed
      $('.pt-container').slick('resize');

      //reset event listener on resize
      $('.slick-next').on('click', function() {
        $('.slick-prev').addClass('active');
      });

      if ($(window).width() >= 768 && !($('.top-nav').hasClass('right'))) {
        $('.top-nav').addClass('right');
      }
    });

    $('.toggle').on('click',function(){
      $(this).toggleClass('active');
    });

    var forwarding = window.location.hash.replace("#","");
    if (forwarding) {
        $("#generalInstructions").hide();
        $("#continueEdit").show();
        $("#continueEditButton").text("Edit " + forwarding);
        $("#continueEditButton").attr("href", "{{ site.githuburl }}edit/master/" + forwarding)
    } else {
        $("#generalInstructions").show();
        $("#continueEdit").hide();
    }
});

// Prettyprint
$('pre').addClass("prettyprint");
$.getScript("https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js", function(){
});

// Collapsible navbar menu, using https://github.com/jordnkr/collapsible
$.getScript("/crmint/js/jquery.collapsible.js", function(){
  highlightActive();
  $('.submenu').collapsible();
});

// TOC script
// https://github.com/ghiculescu/jekyll-table-of-contents
(function($){
  $.fn.toc = function(options) {
    var defaults = {
      noBackToTopLinks: false,
      title: '',
      minimumHeaders: 2,
      headers: 'h2, h3, h4, h5, h6',
      listType: 'ol', // values: [ol|ul]
      showEffect: 'show', // values: [show|slideDown|fadeIn|none]
      showSpeed: 'slow' // set to 0 to deactivate effect
    },
    settings = $.extend(defaults, options);

    function fixedEncodeURIComponent (str) {
      return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
        return '%' + c.charCodeAt(0).toString(16);
      });
    }

    var headers = $(settings.headers).filter(function() {
      // get all headers with an ID
      var previousSiblingName = $(this).prev().attr( "name" );
      if (!this.id && previousSiblingName) {
        this.id = $(this).attr( "id", previousSiblingName.replace(/\./g, "-") );
      }
      return this.id;
    }), output = $(this);
    if (!headers.length || headers.length < settings.minimumHeaders || !output.length) {
      return;
    }

    if (0 === settings.showSpeed) {
      settings.showEffect = 'none';
    }

    var render = {
      show: function() { output.hide().html(html).show(settings.showSpeed); },
      slideDown: function() { output.hide().html(html).slideDown(settings.showSpeed); },
      fadeIn: function() { output.hide().html(html).fadeIn(settings.showSpeed); },
      none: function() { output.html(html); }
    };

    var get_level = function(ele) { return parseInt(ele.nodeName.replace("H", ""), 10); }
    var highest_level = headers.map(function(_, ele) { return get_level(ele); }).get().sort()[0];
    var return_to_top = '<i class="icon-arrow-up back-to-top"> </i>';

    var level = get_level(headers[0]),
      this_level,
      html = settings.title + " <"+settings.listType+">";
    headers.on('click', function() {
      if (!settings.noBackToTopLinks) {
        window.location.hash = this.id;
      }
    })
    .addClass('clickable-header')
    .each(function(_, header) {
      this_level = get_level(header);
      if (!settings.noBackToTopLinks && this_level === highest_level) {
        $(header).addClass('top-level-header').after(return_to_top);
      }
      if (this_level === level) // same level as before; same indenting
        html += "<li><a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
      else if (this_level <= level){ // higher level than before; end parent ol
        for(i = this_level; i < level; i++) {
          html += "</li></"+settings.listType+">"
        }
        html += "<li><a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
      }
      else if (this_level > level) { // lower level than before; expand the previous to contain a ol
        for(i = this_level; i > level; i--) {
          html += "<"+settings.listType+"><li>"
        }
        html += "<a href='#" + fixedEncodeURIComponent(header.id) + "'>" + header.innerHTML + "</a>";
      }
      level = this_level; // update for the next one
    });
    html += "</"+settings.listType+">";
    if (!settings.noBackToTopLinks) {
      $(document).on('click', '.back-to-top', function() {
        $(window).scrollTop(0);
        window.location.hash = '';
      });
    }

    render[settings.showEffect]();
  };
})(jQuery);
