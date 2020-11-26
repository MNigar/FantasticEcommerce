$(function () {


    $("#Forms").validate({
        rules: {
            //name: "required",

            Name: {
                required: true,
                minlength: 3,
                lettersonly: true
            },
            Surname: {
                required: true,
                minlength: 3,
                lettersonly: true
            },
            Username: {
                required: true,
                minlength: 4
               
            },
            Email: {
                required: true,
                emailcheck:true,
               
            },
            Password: {
                required: true,
                minlength: 4,
                check: true,
            },
            Phone: {
                required: true
               
               
            },
            exampleCheck1:{
                required: true,
            }
            
        },
        messages: {
            Name: {
                required: "Adı daxil edin",
                minlength: "Minimum simvol sayı 3",
                lettersonly: "Yalnız hərflərdən istifadə edə bilərsiniz"
            },
            Surname: {
                required: "Soyadı daxil edin",
                minlength: "Minimum simvol sayı 3",
                 lettersonly: "Yalnız hərflərdən istifadə edə bilərsiniz"
            },
            Username: {
                required: "Istifadəçi adı daxil edin",
                 minlength: "Minimum simvol sayı 4"

            },
            Email: {
                required: "Elektron poçtunuzu daxil edin",
                emailcheck:" Emailiniz example@example.example formatinda olmalidir "
            },
            Password: {
                required: "Şifrəni daxil edin",
                minlength: "Minimum simvol sayı 4",
                check:" Yalnız Hərflər rəqəmlər və !\-@._* simvollarından istifadə edə bilərsiniz "
            },
            Phone: {
                required: "Nömrəni daxil edin",
                
            },
            exampleCheck1:{
                required: "İşarələyin"
            }
            

        },

    });
    $.validator.addMethod("check",
        function (value, element) {
            return /^[A-Za-z0-9\d=!\-@._*]+$/.test(value);
        });
    $.validator.addMethod("emailcheck",
        function (value, element) {
            return /^[a-z0-9][-a-z0-9._]+@([-a-z0-9]+[.])+[a-z]{2,5}$/.test(value);
        });
    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return  /^[A-Za-z]+$/.test(value);
    }); 
});
