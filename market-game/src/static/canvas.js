$('.pixel').on('click', e=>{
    pixel=$(e.currentTarget)
    $('#x-value').val(pixel.attr('x'))
    $('#y-value').val(pixel.attr('y'))
    $('#x-holder').text(pixel.attr('x'))
    $('#y-holder').text(pixel.attr('y'))
    $('#example-pixel').css('color','black')
    //console.log(e.pageX,e.pageY)
})
$('.color').keyup(e=>{
    r=Math.floor(Number($('#red').val())/100*256).toString()
    g=Math.floor(Number($('#green').val())/100*256).toString()
    b=Math.floor(Number($('#blue').val())/100*256).toString()
    console.log(r,g,b)
    color=r+','+g+','+b
    $('#color-picker').css('background-color', 'rgb('+color+',.8)')
})
