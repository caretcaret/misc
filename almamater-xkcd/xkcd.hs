-- cabal install skein
import Data.Char
import Crypto.Skein
import Crypto.Classes
import Data.Serialize
import Data.Hex
import Data.ByteString.Lazy.Char8 (pack)

strs = map (\x -> [x]) "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789."
str = ""
main = print . hex . encode . (hash . pack :: String -> Skein_1024_1024) $ str
