class TemplateMail(object):
    SUBJECT_MAIL_REGISTER_ACCOUNT = 'MSRV - Xác minh đăng ký tài khoản'
    SUBJECT_MAIL_RESET_PASSWORD = 'MSRV - Xác nhận đặt lại mật khẩu'

    CONTENT_MAIL_REGISTER_ACCOUNT = lambda full_name, otp_code: F"""<div>
    <p>Xin chào {full_name},</p>
    <p>Chào mừng bạn đến với MSRV! Để hoàn tất quá trình đăng ký tài khoản, vui lòng sử dụng mã OTP sau: <strong>{otp_code}</strong>.</p>
    <p>Mã OTP này có hiệu lực trong một khoảng thời gian giới hạn. Vui lòng không chia sẻ mã này với bất kỳ ai.</p>
    <p>Trân trọng,</p>
    <p>Đội ngũ MSRV</p>
  </div>"""

    CONTENT_MAIL_RESET_PASSWORD = lambda full_name, otp_code: F"""<div>
    <p>Xin chào {full_name},</p>
    <p>Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản MSRV của mình. Vui lòng sử dụng mã OTP sau để xác nhận: <strong>{otp_code}</strong>.</p>
    <p>Nếu bạn không yêu cầu thay đổi mật khẩu, vui lòng bỏ qua email này.</p>
    <p>Trân trọng,</p>
    <p>Đội ngũ MSRV</p>
  </div>"""
