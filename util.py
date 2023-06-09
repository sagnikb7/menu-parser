counter = 0
def cleanup(sentences):
    global counter
    result = []
    clean_items = []
    for s in sentences:

        # s1,s2 = detectSub(s)
        # if s1 != False and s2 != False:
        #     clean_items.append(s1)
        #     clean_items.append(s2)
        sub = detectSubSimple(s)
        if sub != False:
            for s0 in sub:
                clean_items.append(s0.strip())
        
        elif s != "":
            clean_items.append(s.strip())

    items = []
    price = []
    for c in clean_items:
        try:
            f = float(c)
            price.append(f)
        except ValueError:
            items.append(c)
    if len(items) == len(price):
        for i in range(len(items)):
            counter+=1
            result.append({"id":counter, "item":items[i], "price":price[i]})
    else:
        print("DEBUG 1-> ",sentences)
        print("DEBUG 2->",len(items),len(price))
        print("DEBUG 3-> ",clean_items)
    # TODO remove
    for r in result:
        print(r)
    return result

def detectSubSimple(input_string):
    if "/" in input_string:
        result_array = input_string.split("/")
        # if len(result_array) > 1:
        #     master_item = result_array[0]
        #     for i,x in enumerate(result_array):
        #         if i == 0:
        #             continue
        #         if master_item not in x:
        #             result_array[i] = master_item.strip()+" "+x.strip() 
        return result_array
    return False
