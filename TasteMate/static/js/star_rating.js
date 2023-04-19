document.querySelector('.rating ul li').addEventListener('click', function() {

    let li = document.querySelector(this),
        ul = li.parent(),
        rating = ul.parent(),
        last = ul.querySelector('.current');

    if(!rating.classList.contains('animate-left') && !rating.classList.contains('animate-right')) {

        last.classList.remove('current');

        ul.children('li').each(function() {
            let current = document.querySelector(this);
            current.classList.toggle('active', li.index() > current.index());
        });

        rating.classList.add(li.index() > last.index() ? 'animate-right' : 'animate-left');
        rating.css({
            '--x': li.position().left + 'px'
        });
        li.classList.add('move-to');
        last.classList.add('move-from');

        setTimeout(() => {
            li.classList.add('current');
            li.classList.remove('move-to');
            last.classList.remove('move-from');
            rating.classList.remove('animate-left animate-right');
        }, 800);

    }

})
