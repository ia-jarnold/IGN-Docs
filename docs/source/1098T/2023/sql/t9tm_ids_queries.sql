/****** Object:  Table [dbo].[CAST_SP_RPT]    Script Date: 1/16/2024 2:46:33 PM ******/
/*SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[L56_1098T_T9TM_IDS](
	[T9_SSN] [VARCHAR](9) NULL,
	[T9_ID] [VARCHAR](7) NULL
)*/

SELECT *
FROM L56_1098T_T9TM_IDS

UPDATE t9
SET t9.T9_SSN = NULL
FROM L56_1098T_T9TM_IDS t9
WHERE t9.T9_SSN = ''

TRUNCATE L56_1098T_T9TM_IDS -- wizard can do this too but no term/year/date info is kept atm.