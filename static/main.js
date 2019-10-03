
$(function() {

    $("#file").on('change', function(event) {
        let image = document.getElementById('output');
        image.src = URL.createObjectURL(event.target.files[0]);
        $('#myButton, .section-input-firstname').removeClass('hidden')
    }); 

    $("#myButton").on('click', function(e)
    {
        // e.preventDefault();
        // if ($('.input-firstname').val() != '' ) {
        // $('#form-predict-correction').trigger('submit')
        // }
        $('#form-predict-correction').trigger('submit')
    });
    function renderMusic(music){
        let name = music[1] + " - " + music[2]; 
        return `
        <li>
            <button class="myBtn" id=${music[3]} onclick="newMusic" type="button">${name}</button>
        </li>
        `
    }

    $('#form-predict-correction').on('submit', function(e) {
        e.preventDefault();
        let my_form = document.getElementById('form-predict-correction')
        let form_data = new FormData(my_form);
        
        let image = document.getElementById('output');
        
        console.log(form_data);

        $.ajax({
            type: 'POST',
            url: '/upload/',
            processData: false,
            contentType: false,
            data: form_data,
            success: function(data) {
                $('#form-predict-correction .button,.section-input-firstname').addClass('hidden')
                console.log()
                $('#output').attr('src', 'data:image/jpg;base64,' + data['img'])
                // initYoutube();
                $('#player').removeClass('hidden')
                player.loadVideoById(data['videoId'])
                player.playVideo()
                console.log(data['videoId'])
                
                const articles = data['song'];
                console.log(data['song'])
                const articlesHTML = articles.map(renderMusic).join('');
                document.getElementById('newsList').innerHTML = articlesHTML;

                
                document.addEventListener('click', function(e){
                    if(e.target.tagName=="BUTTON"){
                        player.loadVideoById(e.target.id);
                        player.playVideo();
                    }
                  })
            }
        });
    });

    
});

