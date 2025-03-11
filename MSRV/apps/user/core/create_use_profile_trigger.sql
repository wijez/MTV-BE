CREATE OR REPLACE FUNCTION create_user_profile()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.user_userprofile (user_id, degree, department, country, address, nation, nationality, religion, created_at, updated_at)
    VALUES (
        NEW.id,
        'TS',  -- Giá trị mặc định của DegreeEnum (thay đổi nếu cần)
        'INFORMATION_TECHNOLOGY', -- Giá trị mặc định của DepartmentEnum (thay đổi nếu cần)
        '', '', '', '', '',
        NOW(), NOW()
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Xóa trigger cũ nếu có
DROP TRIGGER IF EXISTS after_user_insert ON public.auth_user;

-- Tạo trigger mới
CREATE TRIGGER after_user_insert
AFTER INSERT ON public.user_user
FOR EACH ROW
EXECUTE FUNCTION create_user_profile();
