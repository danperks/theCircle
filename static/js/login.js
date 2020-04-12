function addGap() {
    nav = document.getElementById("mainnav");
    li = document.createElement("li");
    a = document.createElement("a")
    li.appendChild(a);
    i = document.createElement("i")
    a.appendChild(i)
    p = document.createElement("p")
    a.appendChild(p)
    nav.appendChild(li);
}

function addLogin(status) {
    if (status == true) {
        nav = document.getElementById("mainnav");
        li = document.createElement("li");
        li.className = "active-pro"
        a = document.createElement("a")
        a.href = "/api/logout"
        li.appendChild(a);
        i = document.createElement("i")
        i.className = "now-ui-icons objects_key-25"
        a.appendChild(i)
        p = document.createElement("p")
        p.innerHTML = "Logout"
        a.appendChild(p)
        nav.appendChild(li);
    } else {
        nav = document.getElementById("mainnav");
        li = document.createElement("li");
        li.className = "active-pro"
        a = document.createElement("a")
        a.href = "/accounts"
        li.appendChild(a);
        i = document.createElement("i")
        i.className = "now-ui-icons objects_key-25"
        a.appendChild(i)
        p = document.createElement("p")
        p.innerHTML = "Signup / Login"
        a.appendChild(p)
        nav.appendChild(li);
    }
}

function addtoSidebar(icon, text, href, active) {
    nav = document.getElementById("mainnav");
    li = document.createElement("li");
    if (active) {
        li.className = "active";
    }
    a = document.createElement("a");
    a.href = href;
    li.appendChild(a);
    i = document.createElement("i");
    i.className = "now-ui-icons " + icon;
    a.appendChild(i);
    p = document.createElement("p");
    p.innerHTML = text;
    a.appendChild(p);
    nav.appendChild(li);
}

function addUserOptions(status, active) {
    addtoSidebar("location_compass-05", "Home", "/", active[0]);
    addtoSidebar("design_bullet-list-67", "Request a Slot", "/book", active[1]);
    addtoSidebar("shopping_tag-content", "Add a Shop", "/addashop", active[3]);
    addGap()
    addLogin(status)
}

function addBusinessOptions(status, active) {
    addtoSidebar("design_app", "Dashboard", "/business/dashboard", active[0]);
    addtoSidebar("tech_mobile", "Scan QR Codes", "/business/qr", active[1]);
    addGap();
    addtoSidebar("location_map-big", "Browse Map", "/browse", active[2]);
    addLogin(status);
}

function getCookie(name) {
    var dc = document.cookie;
    var prefix = name + "=";
    var begin = dc.indexOf("; " + prefix);
    if (begin == -1) {
        begin = dc.indexOf(prefix);
        if (begin != 0) return null;
    } else {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
            end = dc.length;
        }
    }
    return decodeURI(dc.substring(begin + prefix.length, end));
}

function init(user, business, forceGPS, forceUser, forceBusiness) {
    var auth = getCookie("auth");
    var bauth = getCookie("bauth");
    if (auth == null && bauth == null) { // no auth tokens
        addUserOptions(false, user);


    } else {
        if (auth == null) { // business user
            addBusinessOptions(true, business)
        } else { // regular user
            addUserOptions(true, user)
        }

    }
}